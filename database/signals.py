import textwrap
from pathlib import Path
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from database.models import PesticidalProteinDatabase


def filter_files_ending_with_one(SUBJECT_FASTAFILES):
    """
    The function filters the files end with 1
    """
    return [
        name for name in SUBJECT_FASTAFILES if name[-1].isdigit() and not name[-2].isdigit() == 1 and int(name[-1]) == 1
    ]


def write_files(objectname):
    path = Path(settings.MEDIA_ROOT, "run_bestmatchfinder/")
    print("path", path)
    for protein in objectname:
        file = protein.name + ".txt"
        name = str(path) + "/" + file
        with open(name, "wb") as file:
            fasta = textwrap.fill(protein.sequence, 80)
            str_to_write = f">{protein.name}\n{fasta}\n"
            file.write(str_to_write.encode())


@receiver(post_save, sender=PesticidalProteinDatabase)
def update_files(sender, instance, **kwargs):
    proteins = PesticidalProteinDatabase.objects.values_list(
        "name", flat=True)
    protein_endwith1 = filter_files_ending_with_one(list(proteins))

    # private_proteins = PesticidalProteinPrivateDatabase.objects.values_list(
    #     'name', flat=True)
    proteins_filtered = PesticidalProteinDatabase.objects.filter(
        name__in=protein_endwith1)
    write_files(proteins_filtered)


#post_save.connect(update_files, sender=PesticidalProteinDatabase)
