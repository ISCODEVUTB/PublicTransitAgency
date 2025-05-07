import pytest
from backend.app.models.rutaparada import RutaParada

def test_rutaparada_creation():
    """
    Prueba la creación de una instancia de RutaParada.
    """
    rutaparada = RutaParada(id=1, idruta=2, idparada=3)
    assert rutaparada.id == 1
    assert rutaparada.idruta == 2
    assert rutaparada.idparada == 3

def test_rutaparada_to_dict():
    """
    Prueba la conversión de una instancia de RutaParada a un diccionario.
    """
    rutaparada = RutaParada(id=1, idruta=2, idparada=3)
    rutaparada_dict = rutaparada.to_dict()
    assert isinstance(rutaparada_dict, dict)
    assert rutaparada_dict["id"] == 1
    assert rutaparada_dict["idruta"] == 2
    assert rutaparada_dict["idparada"] == 3

def test_rutaparada_from_dict():
    """
    Prueba la creación de una instancia de RutaParada a partir de un diccionario.
    """
    data = {"id": 1, "idruta": 2, "idparada": 3}
    rutaparada = RutaParada.from_dict(data)
    assert rutaparada.id == 1
    assert rutaparada.idruta == 2
    assert rutaparada.idparada == 3

def test_rutaparada_get_fields():
    """
    Prueba la obtención de los campos de la tabla RutaParada.
    """
    fields = RutaParada.get_fields()
    assert isinstance(fields, dict)
    assert "id" in fields
    assert "idruta" in fields
    assert "idparada" in fields
    assert fields["id"] == "INTEGER PRIMARY KEY"
    assert fields["idruta"] == "INTEGER NOT NULL"
    assert fields["idparada"] == "INTEGER NOT NULL"