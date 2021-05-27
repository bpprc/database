from django.urls import resolve, reverse

from bestmatchfinder import views


class TestUrls:
    def test_graphs_home(self):
        path = reverse("graphs_home")
        assert resolve(path).view_name == "graphs_home"

    def test_combo(self):
        path = reverse("combo")
        assert resolve(path).view_name == "combo"

    def test_programming(self):
        path = reverse("programming")
        assert resolve(path).view_name == "programming"

    def test_multiplot(self):
        path = reverse("multiplot")
        assert resolve(path).view_name == "multiplot"

    def test_pie(self):
        path = reverse("pie")
        assert resolve(path).view_name == "pie"

    def test_protein_table(self):
        path = reverse("protein_table")
        assert resolve(path).view_name == "protein_table"
