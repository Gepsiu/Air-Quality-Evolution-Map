import json
import tempfile
from unittest.mock import patch, mock_open

from django.test import TestCase, Client
from django.urls import reverse
from map.models import Measurement, Legend, LegendLevel, Station
from map.views import load_coord, build_pollution_scale


class LoadCoordTests(TestCase):

    def test_load_coord_valid_json(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as f:
            json.dump({"a": 1}, f)
            f.flush()
            result = load_coord(f.name)
        self.assertEqual(result, {"a": 1})

    def test_load_coord_missing_file(self):
        with self.assertRaises(RuntimeError) as ctx:
            load_coord("non_existing_file.json")
        self.assertIn("Brak pliku", str(ctx.exception))

    def test_load_coord_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as f:
            f.write("{ invalid json }")
            f.flush()
            with self.assertRaises(RuntimeError) as ctx:
                load_coord(f.name)
        self.assertIn("Błąd JSON", str(ctx.exception))

    def test_load_coord_mocked_json(self):
        mock_data = {"test": "value"}
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = load_coord("fake_path.json")
        self.assertEqual(result, mock_data)


class BuildPollutionScaleTests(TestCase):
    def setUp(self):
        self.legend = Legend.objects.create(pollutant="PM10", unit="µg/m³")
        LegendLevel.objects.create(legend=self.legend, order=1, limit=20, label="Good", color="#00ff00")
        LegendLevel.objects.create(legend=self.legend, order=2, limit=50, label="Bad", color="#ff0000")

    def test_build_pollution_scale_returns_dict(self):
        result = build_pollution_scale()
        self.assertIsInstance(result, dict)

    def test_build_pollution_scale_contains_pollutant(self):
        result = build_pollution_scale()
        self.assertIn("PM10", result)

    def test_build_pollution_scale_contains_unit(self):
        result = build_pollution_scale()
        self.assertEqual(result["PM10"]["unit"], "µg/m³")

    def test_build_pollution_scale_contains_limits(self):
        result = build_pollution_scale()
        self.assertEqual(result["PM10"]["limits"], [20, 50])

    def test_build_pollution_scale_contains_labels(self):
        result = build_pollution_scale()
        self.assertEqual(result["PM10"]["labels"], ["Good", "Bad"])

    def test_build_pollution_scale_contains_colors(self):
        result = build_pollution_scale()
        self.assertEqual(result["PM10"]["colors"], ["#00ff00", "#ff0000"])

    def test_build_pollution_scale_empty(self):
        Legend.objects.all().delete()
        result = build_pollution_scale()
        self.assertEqual(result, {})


class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.station = Station.objects.create(code="ST001", voivodeship="Mazowieckie")
        Measurement.objects.create(pollutant="PM10", measurement_date="2024-01-01", station=self.station,
                                   measurement_value=10)

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_status_code(self, mock_scale, mock_coord):
        mock_coord.return_value = {}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertEqual(response.status_code, 200)

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_template(self, mock_scale, mock_coord):
        mock_coord.return_value = {}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertTemplateUsed(response, "map/map.html")

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_contains_pollution(self, mock_scale, mock_coord):
        mock_coord.return_value = {}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertIn("pollution", response.context)

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_contains_years(self, mock_scale, mock_coord):
        mock_coord.return_value = {}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertIn("years", response.context)

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_contains_geojson(self, mock_scale, mock_coord):
        mock_coord.return_value = {"geo": "json"}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertEqual(response.context["geojson"], {"geo": "json"})

    @patch("map.views.load_coord")
    @patch("map.views.build_pollution_scale")
    def test_main_view_contains_coord_provinces(self, mock_scale, mock_coord):
        mock_coord.return_value = {"coord": "data"}
        mock_scale.return_value = {}
        response = self.client.get(reverse("map:map"))
        self.assertIn(
            "coord_provinces",
            response.context
        )


class MapDataViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("map.views.MeasurementAgg")
    def test_map_data_status_code_success(self, mock_model):
        mock_model.objects.filter.return_value.values.return_value = [
            {
                "voivodeship": "Mazowieckie",
                "avg_value": 42.5
            }
        ]
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "year": "2024",
                "month": "1"
            }
        )
        self.assertEqual(response.status_code, 200)

    @patch("map.views.MeasurementAgg")
    def test_map_data_returns_json(self, mock_model):
        mock_model.objects.filter.return_value.values.return_value = [
            {
                "voivodeship": "Mazowieckie",
                "avg_value": 42.5
            }
        ]
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "year": "2024",
                "month": "1"
            }
        )
        self.assertEqual(response.json(), {"Mazowieckie": 42.5})

    def test_map_data_missing_pollutant(self):
        response = self.client.get(
            reverse("map:map_data"),
            {
                "year": "2024",
                "month": "1"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_map_data_missing_year(self):
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "month": "1"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_map_data_missing_month(self):
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "year": "2024"
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch("map.views.MeasurementAgg")
    def test_map_data_empty_queryset(self, mock_model):
        mock_model.objects.filter.return_value.values.return_value = []
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "SO2",
                "year": "2024",
                "month": "1"
            }
        )
        self.assertEqual(response.json(), {})

    def test_map_data_invalid_month(self):
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "year": "2024",
                "month": "13"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_map_data_invalid_year(self):
        response = self.client.get(
            reverse("map:map_data"),
            {
                "pollutant": "PM10",
                "year": "abcd",
                "month": "1"
            }
        )
        self.assertEqual(response.status_code, 400)
