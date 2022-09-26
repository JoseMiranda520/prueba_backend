from app.serializers import *
from django.contrib.auth.models import Group
from app.models import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from django.views.generic import ListView, DetailView

""" IMPORT FILTERS """
from django_filters import rest_framework 
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from .filters import *

from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.http import Http404, HttpResponseNotAllowed

from django.db.models import Count, Case, When, IntegerField, Sum, F, Avg
from django.db.models.query import QuerySet

""" IMPORT FILTERS """
from django.core import serializers
import json, calendar
from datetime import datetime, date, time, timedelta
import logging 
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog


User = get_user_model()

# Create your views here.
class UserViewSet(LoggingMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_class = UserFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    """
    # Registro de visitas por dia.
    @action(detail=False, methods=['GET'])
    def visit_for_day(self, request):
        date = datetime.now()
        year = (date.year)
        month = (date.month)
        day = (date.day)
        date = str(year) + ('-') + str(month) + ('-') + str(day)
        queryset = User.objects.filter(last_login__contains=date)
        queryset = queryset.values('last_login')
        queryset = len(queryset)
        return Response({'visitforday': queryset})
"""

class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LinkViewSet(viewsets.ModelViewSet):

    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    filter_class = LinkFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    filter_class = ProfileFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def retrieve_profile(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'No tienes permisos para hacer esta consulta.'})
        user = self.request.query_params.get('user', None)
        if user == None:
            return Response({'detail': 'Se debe indicar el asesor a consultar.'})
        try:
            profile = Profile.objects.get(user__username=user)
            profile = ProfileDetailedSerializer(profile, context={'request': request}).data
            return Response({'profile': profile})
        except Exception:
            return Response({'detail': 'No existe este perfil.'})

    @action(detail=False, methods=['GET'])
    def get_my_profile(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile:
            pilots = PilotSerializer(profile.pilot, many=True).data
            profile = ProfileSerializer(profile, context={'request': request}).data
            return Response({'profile': profile, 'pilots': pilots})
        else:
            return Response({'detail': 'No existe este perfil.'})

    @action(detail=True, methods=['POST'])
    def set_avatar(self, request, pk):
        try:
            if 'file' in request.FILES:
                profile = Profile.objects.get(id=pk)
                avatar = request.FILES['file']
                profile.avatar = avatar
                profile.save()
            else:
                return Response({'detail': 'No se ha agregado ningún archivo'})
            return Response({
                'detail':'success',
                'new_route': str(profile.avatar.url)
                })
        except  ValidationError:
            return Response({'detail': 'Formato inválido'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PublishViewSet(viewsets.ModelViewSet):

    queryset = Publish.objects.all()
    serializer_class = PublishSerializer
    filter_class = PublishFilter
    filter_backends = (SearchFilter, filters.DjangoFilterBackend, OrderingFilter,)
    search_fields = ('title', 'short_description', 'description', 'tags__name')
    
    @action(detail=False, methods=['GET'])
    def weekly_top(self, request):
        allowed_pilots = ProfileSerializer(Profile.objects.get(user=request.user), context={'request': request}).data['pilot']
        query_pilot = self.request.query_params.get('pilot', None)
        if  query_pilot == None:
            return Response({'detail': 'Debes incluir un piloto en el query'})
        last_ten_publishes = []
        if int(query_pilot) in allowed_pilots:
            last_ten_publishes = PublishSerializer(Publish.objects.filter(assign_byPilot=query_pilot)[:10], many=True).data
        return Response({'obj': last_ten_publishes})
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublishListSerializer
        return PublishSerializer


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_class = TagFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)


class PilotViewSet(viewsets.ModelViewSet):

    serializer_class = PilotSerializer
    queryset = Pilot.objects.all()

    filter_class = PilotFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)


class AlertViewSet(viewsets.ModelViewSet):
 
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    
    filter_class = AlertFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def get_alerts1(self, request):
        # ---------------  Paso 1: Get Pilot
        try:
            pilot = self.request.query_params.get('pilot')
            if pilot == None: raise ValidationError('Un piloto debe ser indicado para hacer la consulta.')
            pass
        except ValidationError:
            # End process.
            return Response({'detail': 'Un piloto debe ser indicado para hacer la consulta.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # ---------------  Paso 2: Get Quiz Status
        quiz_status = {'quiz_exists_flag': False}
        try:
            pilot = Pilot.objects.get(id=pilot)
            # Obtengo el último quiz creado para el piloto del query, si no hay: excepción IndexError:
            last_quiz_by_pilot = Quiz.objects.order_by('-id').filter(assign_byPilot=pilot)[0]
            quiz_result_related = Quiz_result.objects.get_or_create(user=request.user, quiz=last_quiz_by_pilot, pilot_id=pilot.id)[0]
            # Adjuntamos los datos relevantes del Quiz
            quiz_status.update({
                'quiz_exists_flag': True,
                'status_pending_quiz': False,
                'quiz_result_id': quiz_result_related.id,
                'grade': quiz_result_related.result,
                'quiz_id': last_quiz_by_pilot.id,
                'quiz_name': last_quiz_by_pilot.name,
                'finish_date': last_quiz_by_pilot.finish_date
            })
            if quiz_result_related.result is '' or quiz_result_related.result is None:
                quiz_status['status_pending_quiz'] = True
                try:
                    # Validamos el schedule programado, si aun no supera la hora programada no manda alerta
                    quiz_status['do_it_now'] = quiz_result_related.schedule.astimezone(tz=None).isoformat() < datetime.now().isoformat()
                    pass
                except AttributeError:
                    # Excepción para cuando no hay un schedule programado, manda alerta
                    quiz_status['do_it_now'] = True
                    pass
                
            pass
        except IndexError:
            # No se encontró ningún quiz.
            pass
        except MultipleObjectsReturned:
            quiz_status['quiz_exists_flag'] = 'Multiple'
            # Se encontró más de un Quiz.
            pass

        #---------------- Paso 3: Get Alerts
        filtered_alerts = Alert.objects.filter(pilot=pilot).order_by('-date')
        serialized_alerts = AlertSerializer(filtered_alerts, many=True).data

        #---------------- Paso 4: Return data.
        return Response({'alerts': serialized_alerts, 'quiz_status': quiz_status})


class QuizViewSet(viewsets.ModelViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    filter_class = QuizFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def last_quiz(self, request):
        pilot = self.request.query_params.get('pilot', None)
        if pilot is None:
            return Response({'detail': 'Debe elegirse un piloto para realizar el quiz.'})
        try:
            last_quiz = Quiz.objects.all().filter(assign_byPilot=pilot).order_by('-id')[0]
            pass
        except IndexError:
            return Response({'detail': 'No ha sido creado ningún quiz aún.'})
        piloto = Pilot.objects.get(id=pilot)
        quiz_result_related = Quiz_result.objects.get_or_create(user=request.user, quiz=last_quiz, pilot=piloto)[0]
        if quiz_result_related.result is not '' and quiz_result_related.result is not None:
            return Response({'detail': 'Este Quiz ya fue resuelto.'})

        questions_array = QuestionProductionSerializer(last_quiz.questions, many=True)
        serialized_quiz = QuizSerializer(last_quiz)
        respuesta = []
        respuesta.append(serialized_quiz.data)
        respuesta.append(questions_array.data)
        return Response(respuesta)


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_class = QuestionFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)


class QuizResultViewSet(viewsets.ModelViewSet):

    queryset = Quiz_result.objects.all()
    serializer_class = QuizResultSerializer
    filter_class = QuizResultFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

    def perform_create(self, serializer):
        user = self.request.user
        quiz = serializer.validated_data['quiz']
        if Quiz_result.objects.filter(quiz=quiz, user=user).exists():
            raise Http404
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        try:
            newSchedule = serializer.validated_data.get('schedule', None)
            if newSchedule:
                limitDate = serializer.validated_data['quiz'].finish_date
                if newSchedule.isoformat() < limitDate.isoformat():
                    serializer.save()
                else:
                    raise ValueError("La fecha introducida supera la máxima permitida: " + limitDate.isoformat())
        except ValueError:
            return Response({'detail': 'Fecha no permitida'})

    @action(detail=False, methods=['POST'])
    def send_answers(self, request):
        try:
            user_answers = json.loads(self.request.query_params.get('answers', None))
            quiz = int(self.request.query_params.get('quiz', None))
            quiz_object = Quiz.objects.get(id=quiz)
            questions = QuestionSerializer(quiz_object.questions, many=True).data
            quiz_grade = float(0)

            if len(questions) != len(user_answers):
                return Response({'detail': str("Error: Fueron enviadas {0} respuestas y se esperaban {1}".format(len(user_answers), len(questions)))})

            quiz_result_related = Quiz_result.objects.get_or_create(user=request.user, quiz=quiz)[0]
            if quiz_result_related.result is not '' and quiz_result_related.result is not None:
                raise ValidationError('El quiz que intenta realizar ya fue realizado anteriormente.')

            # Entramos a las preguntas del quiz a buscar los id
            for question_index in range(len(list(questions))):
                # Identificamos cuáles son las opciones y las respectivas respuestas correctas (en el back)
                option_list = json.loads(questions[question_index]['option_list'])
                db_correct_answer = json.loads(questions[question_index]['correct_option'])
                # Si es array hacer ciclo, sino validar directo
                if type(db_correct_answer) == list and type(user_answers[question_index]) == list and questions[question_index]['multiple']:
                    correctas =  0
                    bad_selection = 0
                    user_answers[question_index] = [user_answers[question_index]] if (type(user_answers[question_index]) == int) else user_answers[question_index]
                    for single_ans in list(user_answers[question_index]):
                        if single_ans in db_correct_answer:
                            correctas += 1
                        else:
                            bad_selection += 1
                    checked = len(db_correct_answer) - correctas
                    non_checked = bad_selection
                    final_count = (len(list(option_list))-(checked + non_checked))/len(list(option_list))
                    quiz_grade += final_count
                # Si no es un array salta a este bloque de validación directa
                elif type(db_correct_answer) == int and type(user_answers[question_index]) == int and not questions[question_index]['multiple']:
                    grade = 1
                    if user_answers[question_index] == db_correct_answer:
                        grade = float(1)
                    else:
                        grade = float(0)
                    quiz_grade += grade
                else: raise TypeError('Al menos una de las respuestas enviadas no coincide con el tipo de pregunta (multiple/única) con que fue creada.') 
            quiz_grade = (quiz_grade / len(list(questions)))*100
            # Asignamos los nuevos valores al quiz_result object (quiz_result_related)
            data = {
                "answers": str(user_answers),
                "result": float(quiz_grade),
                "quiz": int(quiz)
            }

            quiz_result_related.answers = str(user_answers)
            quiz_result_related.result = float(quiz_grade)
            quiz_result_related.quiz_id = int(quiz)
            quiz_result_related.schedule = None

            quiz_result_related.save()
            return Response({
                'status': 'El proceso de efectuó correctamente.',
                'nota': float(quiz_grade)})
        except TypeError as e:
            logging.exception(e)
            # Se ingreso un valor errado
            return Response({
                'error': str(e),
                'detail': 'Error en los datos ingresados.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logging.exception(e)
            # Alguno de los datos requeridos no se encontró en la solicitud
            return Response({'detail': err})
        except MultipleObjectsReturned as e:
            logging.exception(e)
            return Response({
                'error': e.__str__(),
                'detail': 'Error: Se encontró más de una respuesta para este Quiz.'})
        except ObjectDoesNotExist:
            return Response({'detail': 'No existe el quiz que intenta realizar.'})
    

    @action(detail=False, methods=['GET'])
    def reports(self, request):
        """ Se puede obtener el reporte por quiz agregando "?quiz=" en el query (url) """
        queryset = Quiz_result.objects
        quiz_param = request.query_params.get('quiz', None)
        if quiz_param:
            queryset = Quiz_result.objects.filter(quiz=request.query_params['quiz'])
        pilots = queryset.values('pilot_id', 'pilot__name').annotate(count=Count('pilot_id'), avg=Avg('result')).order_by('pilot_id')
        pilots = pilots.annotate(winners=Count(Case (When(result__gt=75, then=1), output_field=IntegerField()) ))
        pilots = pilots.annotate(lossers=Count(Case (When(result__lt=75, then=1), output_field=IntegerField()) ))

        total = Quiz_result.objects.all().aggregate(avg=Avg('result'))
         
        return Response({"response" : {'total': total.get('avg'), 'pilots': pilots, 'quiz': quiz_param if quiz_param else 'Todos los quizes'}})


class SaleViewSet(viewsets.ModelViewSet):

    queryset = Sale.objects.all().order_by('-id')
    serializer_class = SaleSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
   
    @action(detail=False, methods=['GET'])
    def reports(self, request):
        """ Puedes solicitar reporte global agregando global=true al query. Debes incluir pilot al query para consultar la meta correspondiente """
        
        query_global = bool(self.request.query_params.get('global', False))
        personal_sales = None
        if query_global and request.user.is_superuser:
            queryset = Sale.objects
        else:
            queryset = Sale.objects.filter(user=request.user.id)
            personal_sales = queryset
        
        queryset = queryset.values('status')
      
        # SELECT STATUS, COUNT(STATUS), SUM(Cto + CBa + Ctv), SUM(UTo + UBa + UTv) FROM app_sale GROUP BY STATUS ORDER BY STATUS ASC

        # Count status
        queryset = queryset.annotate(state=Count('status', output_field=IntegerField()))

        # Sum Cto + CBa + Ctv
        queryset = queryset.annotate(cross=Sum(F('cto') + F('cba') + F('ctv'), output_field=IntegerField()))

        # Sum UTo + UBa + UTv
        queryset = queryset.annotate(ups=Sum(F('uto') + F('uba')  + F('utv'), output_field=IntegerField()))
        
        queryset.query.group_by = ['status']
        sales = SaleSerializer(personal_sales, many = True).data if not (query_global) else 'Las ventas no están incluidas en el reporte global.'
        pilot = self.request.query_params.get('pilot', None)
        if pilot is not None:
            target = Target.objects.get_or_create(pilot_id=pilot)
            target = TargetSerializer(target[0]).data
            pass
        else:
            target = 'No se agrego un piloto al query'
            pass
        return Response({'results': queryset, 'sales': sales, 'target': target})

    @action(detail=False, methods=['GET'])
    def cumes(self, request):
        "Cantidad de ventas en el mes actual"
        date = datetime.now() 
        year = (date.year)
        month = (date.month)
        date = str(year) + ('-') + str(month)
        
        query_global = bool(self.request.query_params.get('global', False))
        personal_sales = None
        if query_global and request.user.is_superuser:
            queryset = Sale.objects
        else:
            queryset = Sale.objects.filter(user=request.user.id, entry__contains=date)
            
            personal_sales = queryset
        
        queryset = queryset.values('status')
      
        # SELECT STATUS, COUNT(STATUS), SUM(Cto + CBa + Ctv), SUM(UTo + UBa + UTv) FROM app_sale GROUP BY STATUS ORDER BY STATUS ASC

        # Count status
        queryset = queryset.annotate(state=Count('status', output_field=IntegerField()))

        # Sum Cto + CBa + Ctv
        queryset = queryset.annotate(cross=Sum(F('cto') + F('cba') + F('ctv'), output_field=IntegerField()))

        # Sum UTo + UBa + UTv
        queryset = queryset.annotate(ups=Sum(F('uto') + F('uba')  + F('utv'), output_field=IntegerField()))
        
        queryset.query.group_by = ['status']
        return Response({'results': queryset})


class TargetViewSet(viewsets.ModelViewSet):
      
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class ScriptViewSet(viewsets.ModelViewSet):

    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
    filter_class = ScriptFilter
    filter_backends = (SearchFilter, filters.DjangoFilterBackend, OrderingFilter,)
    search_fields = ('title', 'text')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScriptListSerializer
        return ScriptSerializer


class EcardViewSet(viewsets.ModelViewSet):
    
    filter_class = EcardFilter
    filter_backends = (SearchFilter, filters.DjangoFilterBackend, OrderingFilter,)
    queryset = Ecard.objects.filter(pilot__isnull=False)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EcardListSerializer
        return EcardSerializer


class CommissionsViewSet(viewsets.ModelViewSet):
        
    queryset = Commissions.objects.all()
    serializer_class = CommissionsSerializer


class IndicatorViewSet(LoggingMixin, viewsets.ModelViewSet):

    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class IndicatorTipViewSet(viewsets.ModelViewSet):

    queryset = Indicators_tip.objects.all()
    serializer_class = IndicatorTipSerializer


class VisitViewset(viewsets.ModelViewSet):
    queryset = APIRequestLog.objects.all()
    serializer_class = VisitSerializer
    
    filter_class = APIRequestLogFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    
    # Registro de visitas por dia.
    @action(detail=False, methods=['GET'])
    def days(self, request):
        from django.utils import timezone
        from django.db.models import Q, Count
        import datetime

        date = request.query_params.get("date")

        if date:
            start_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        else:
            start_date = timezone.now().date()

        end_date = start_date + datetime.timedelta(days=1)

        queryset = self.queryset\
            .distinct()\
            .filter(user__isnull=False, requested_at__gte=start_date, requested_at__lte=end_date)\
            .values('user')

        return Response({'results': len(queryset)})

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    @action(detail=False, methods=['GET'])
    def users(self, request):
        import datetime
        from django.db import connection
        
        param = request.query_params.get("date")

        if param:
            try:
                date = datetime.datetime.strptime(param, "%Y-%m").date()
            except Exception as e:
                logging.exception(e)
                return Response({'error': '{} debe estar en formato YYYY-mm'.format(param), 'results': []})
        else:
            date = datetime.datetime.now()

        cursor = connection.cursor()
        
        query = " SELECT COUNT(requested) users, requested FROM ("\
                "   SELECT COUNT(DATE(requested_at)), user_id AS total, DATE(requested_at) requested "\
                "   FROM rest_framework_tracking_apirequestlog"\
                "   WHERE user_id IS NOT NULL  AND requested_at > '{}-{}-01' AND requested_at < '{}-{}-01'"\
                "   GROUP BY DATE(requested_at), user_id) queryset"\
                " GROUP BY requested;" \
                .format(date.year, date.month, date.year, date.month+1)
            
        cursor.execute(query)

        data = self.dictfetchall(cursor)

        return Response({'results': data})
        

class MediaViewSet(viewsets.ModelViewSet):
    '''
    Vista de multimedia
    '''
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    filter_class = MediaFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

