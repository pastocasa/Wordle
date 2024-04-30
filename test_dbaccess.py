import dbaccess as bd
import pytest

#Sección "y sí, existen, los acabo de hacer"

def test_abrir_conexion_existe():
    func_dbacc = dir(bd)
    assert 'abrir_conexion' in func_dbacc

def test_consulta_generica_existe():
    func_dbacc = dir(bd)
    assert 'consulta_generica' in func_dbacc

def test_modificacion_generica_existe():
    fun_dbacc = dir(bd)
    assert 'modificacion_generica' in fun_dbacc

def test_cargar_jugador_existe():
    func_dbacc = dir(bd)
    assert 'cargar_jugador' in func_dbacc

#Sección útil

@pytest.fixture
def conn_fixture():
    pytest.dbconn = bd.abrir_conexion()

@pytest.mark.usefixtures("conn_fixture")
def test_cargar_jugador():
    jugador = bd.cargar_jugador(pytest.dbconn, "Juancho")
    assert jugador[0][1] == "Juancho"