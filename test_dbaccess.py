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

def test_jugador_existe_existe():
    func_dbacc = dir(bd)
    assert 'jugador_existe' in func_dbacc

def test_buscar_jugador_existe():
    func_dbacc = dir(bd)
    assert 'buscar_jugador' in func_dbacc

def test_cargar_resultado_existe():
    func_dbacc = dir(bd)
    assert 'cargar_resultado' in func_dbacc

def test_obtener_ids_jugadas_existe():
    func_dbacc = dir(bd)
    assert 'obtener_ids_jugadas' in func_dbacc

def test_obtener_palabra_al_azar_existe():
    func_dbacc = dir(bd)
    assert 'obtener_palabra_al_azar' in func_dbacc

#Sección útil

@pytest.fixture
def conn_fixture():
    pytest.dbconn = bd.abrir_conexion()

@pytest.mark.usefixtures("conn_fixture")
def test_cargar_jugador():
    jugador = bd.cargar_jugador(pytest.dbconn, "Juancho")
    assert jugador[0][1] == "Juancho"

@pytest.mark.usefixtures("conn_fixture")
def test_jugador_existe():
    assert bd.jugador_existe(pytest.dbconn, "Juancho") == True

@pytest.mark.usefixtures("conn_fixture")
def test_error_jugador_existe():
    with pytest.raises(ValueError) as err_info:
        bd.cargar_jugador(pytest.dbconn, "Juancho")
    assert str(err_info.value) == "El nombre Juancho ya esta en uso"

@pytest.mark.usefixtures("conn_fixture")
def test_buscar_jugador():
    assert bd.buscar_jugador(pytest.dbconn, "Juancho") == 5

@pytest.mark.usefixtures("conn_fixture")
def test_buscar_jugador_no_existe():
    with pytest.raises(ValueError) as err_info:
        bd.buscar_jugador(pytest.dbconn, "FLDSMDFR")
    assert str(err_info.value) == "FLDSMDFR no existe en la base de datos"

@pytest.mark.usefixtures("conn_fixture")
def test_cargar_resultado():
    resultado = bd.cargar_resultado(pytest.dbconn, 3, 1, 5)
    assert resultado[0][0] == 3
    assert resultado[0][1] == 1
    assert resultado[0][2] == 5

@pytest.mark.usefixtures("conn_fixture")
def test_cargar_resultado_intentos_incorrectos():
    with pytest.raises(ValueError) as err_info:
        bd.cargar_resultado(pytest.dbconn, 3, 1, 7)
    assert str(err_info.value) == "Cantidad de intentos inválida"

@pytest.mark.usefixtures("conn_fixture")
def test_obtener_id_jugada():
    bd.cargar_resultado(pytest.dbconn, 3, 1, 5)
    assert len(bd.obtener_ids_jugadas(pytest.dbconn, 1)) >= 1

@pytest.mark.usefixtures("conn_fixture")
def test_no_hay_palabras_jugadas():
    with pytest.raises(ValueError) as err_info:
        bd.obtener_ids_jugadas(pytest.dbconn, 0)
    assert str(err_info.value) == "El jugador ingresado todavía no jugó"

#def test_obtener_palabra_al_azar():


#a ver si ahora el github hace algo aaaaaaaaaaaaaaa