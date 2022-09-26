from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import views
from django.conf import settings
import requests


# -------------------------------------Servicio MDM metodos GetByParty y GetByAccount -------------------------------------------------------
"""
(Servicio de MDM donde unifica los metodos GetByParty y GetByAccount)
"""

class GetDataClient(views.APIView):
    permission_classes = [AllowAny]


    def get(self, request):

        try:
            permission_name = '{}.{}_{}'.format('auth', 'view', 'group')
            if not request.user.has_perm(permission_name):
                return Response({'detail': 'Acceso inválido.'}, status=403)
        except AttributeError:
            return Response({'detail': 'Acceso inválido.'}, status=403)
        except Exception:
            return Response({'detail': 'Error inesperado validando permisos.'}, status=402)

        identification = request.GET.get('identification', None)
        if not identification:
            return Response('No se encontro documento a consulta, por favor validar datos',status=status.HTTP_400_BAD_REQUEST)
        else:
            document_types = ['/CC', '/NT', '/CE', 'CV']
            req_GetByParty_cc = None
            headers = {'apiKey': settings.APIKEY_WS_UNE}
            url_cc = settings.URL_WS_UNE+identification
            try:
                for document_type in document_types:
                    url_type = url_cc + document_type
                    response = requests.get(url_type, headers=headers, timeout=10)
                    req_GetByParty_cc = response.json()
                    resp = {
                        'apiresponse': '',
                        'dataifo': []
                    }
                    name = ''
                    doc = ''
                    if req_GetByParty_cc.get('code') != '200' or not req_GetByParty_cc.get('code'):
                        pass
                    else:
                        break

                if req_GetByParty_cc.get('code') != '200' or not req_GetByParty_cc.get('code'):
                    resp['apiresponse'] = 'do not info'
                    resp['dataifo'] = []
                    return Response(resp, status=status.HTTP_200_OK)

                resp['apiresponse'] = 'success'
                for party in req_GetByParty_cc['Partys']:
                    if party['Identification'] == identification and party['Status'] == 'Active':
                        if len(party['Person']) > 1:
                            name = '{} {} {} {}'.format(party['Person']['FirstName'], party['Person']['MiddleName'], party['Person']['LastName'], party['Person']['SecondLastName'])
                            identificationType = party['IdentificationType']
                        else:
                            name = '{}'.format(party['Organization']['OrganizationName'])
                            identificationType = party['IdentificationType']
                        doc = party['Identification']
                if identificationType == 'CC':
                    identificationType = 'Cédula de ciudadanía'
                elif identificationType == 'NIT' or identificationType == 'NT' or identificationType == 'NI':
                    identificationType = 'NIT'
                elif identificationType == 'CC':
                    identificationType = 'Pasaporte'
                elif identificationType == 'CE':
                    identificationType = 'Cédula de extranjería'
                else:
                    identificationType = 'Pasaporte' 
                    
                for contrato in req_GetByParty_cc['Accounts']:
                    if contrato['TypeId'] == '1401' and contrato['SourceId'] == '10' and contrato['Status'] == 'Active':
                        data_client = {}
                        data_client['IdentificationType'] = identificationType
                        data_client['ESTADO'] = 'CONEXION'
                        data_client['CONTRATO'] = contrato['Id']
                        data_client['NOMBRE CLIENTE'] = name
                        data_client['CEDULA'] = doc
                        data_client['DIRECCIÓN DE INSTALACIÓN'] = contrato['LocalAddress']['Legacy']['Address']
                        data_client['DEPARTAMENTO'] = contrato['LocalAddress']['GeographicPlace']['Department']['Name']
                        data_client['CIUDAD'] = contrato['LocalAddress']['GeographicPlace']['Municipality']['Name']
                        data_client['ESTRATO'] = contrato['LocalAddress']['Legacy']['Stratification']
                        data_client['ID_LEGADO'] = contrato['Assets'][0]
                        url = settings.URL_ACCOUNT_WS_UNE + '{}/1401'.format(contrato['Id'])
                        response_account = requests.get(url, headers=headers, timeout=10)
                        req_account = response_account.json()
                        products = []
                        if req_account.get('code') == '200':
                            for product in req_account['Products']:
                                p_name = product['Name']
                                p_technology = product['Assets'][0]['MediaType']
                                p_legacy = product['Assets'][0]['ProductOffering']['Legacy']['Name']
                                p_status = product['Assets'][0]['ProductOffering']['Legacy']['Status']
                                products.append('{} - {} - {} - {}'.format(p_name,p_technology,p_legacy,p_status))
                        data_client['SERVICIOS'] = products 
                        resp['dataifo'].append(data_client)
                return Response(resp, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msj':'No se pudo obtener los contratos'}, status=status.HTTP_409_CONFLICT)
        
