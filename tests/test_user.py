import pytest
from django.urls import reverse
from test1.models import Usuario
from django.contrib.auth import authenticate
from django.db import IntegrityError


@pytest.mark.django_db
def test_registro_exitoso(client):

    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass'
    response = client.post(reverse('register'), {'username': username, 'email': email, 'password': password})

    assert response.status_code == 302
    # Verifica que el usuario se ha creado en la base de datos
    assert Usuario.objects.filter(username=username).exists()
    

@pytest.mark.django_db
def test_logeo_exitoso(client):
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass'
    Usuario.objects.create_user(username=username, email=email, password=password)

    # Realiza una solicitud POST al endpoint de inicio de sesión con los datos de usuario
    response = client.post(reverse('login'), {'username': username, 'password': password})

    # Verifica que la respuesta sea un redireccionamiento (código 302) después de un inicio de sesión exitoso
    assert response.status_code == 302

    # Verifica que el usuario está autenticado
    user = authenticate(username=username, password=password)
    assert user is not None and user.is_authenticated
    
    # verificar que después de iniciar sesión, el usuario es redirigido a alguna página específica
    assert response.url == reverse('panel')
    
    
@pytest.mark.django_db
def test_registro_duplicado(client):
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass'
    Usuario.objects.create_user(username=username, email=email, password=password)

    # Intenta crear otro usuario con la misma información
    with pytest.raises(IntegrityError):
        Usuario.objects.create_user(username=username, email=email, password=password)
        
        
@pytest.mark.django_db
def test_login_con_password_erronea(client):
    username = 'testuser'
    password_correcta = 'testpass_correcta'
    password_erronea = 'testpass_erronea'

    Usuario.objects.create_user(username=username, password=password_correcta)

    # Intenta iniciar sesión con credenciales incorrectas
    response = client.post(reverse('login'), {'username': username, 'password': password_erronea})

    assert response.status_code != 302

@pytest.mark.django_db
def test_login_con_usuario_erroneo(client):
    username_correcto = 'testuser'
    username_erroneo = 'testpass_correcta'
    password = 'testpass_erronea'

    Usuario.objects.create_user(username=username_correcto, password=password)

    # Intenta iniciar sesión con credenciales incorrectas
    response = client.post(reverse('login'), {'username': username_erroneo, 'password': password})

    assert response.status_code != 302