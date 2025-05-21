from django.db import models


class Joueur(models.Model):
    """
    Modèle représentant un joueur de football.

    :ivar id_J: Identifiant unique du joueur (clé primaire).
    :vartype id_J: int

    :ivar nom: Nom complet du joueur.
    :vartype nom: str

    :ivar age: Âge du joueur.
    :vartype age: int

    :ivar poste: Poste occupé par le joueur sur le terrain.
                 Choix possibles : "GK" (Gardien), "DEF" (Défenseur), "MID" (Milieu), "ATT" (Attaquant).
    :vartype poste: str

    :ivar nationalite: Nationalité du joueur.
    :vartype nationalite: str

    :ivar pied_fort: Pied fort du joueur.
                     Choix possibles : "D" (Droit), "G" (Gauche), "O" (Ousmane Dembélé).
    :vartype pied_fort: str

    :ivar nombre_but: Nombre de buts marqués par le joueur.
    :vartype nombre_but: int
    """

    POSTE_CHOICES = [("GK", "Gardien"), ("DEF", "Défenseur"), ("MID", "Milieu"), ("ATT", "Attaquant")]

    PIED_FORT_CHOICES = [("D", "Droit"), ("G", "Gauche"), ("O", "Ousmane Dembélé")]

    id_J = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    age = models.IntegerField()
    poste = models.CharField(
        max_length=3,
        choices=POSTE_CHOICES,  # Appliquer les choix possibles
        default="MID",  # Valeur par défaut
    )
    nationalite = models.CharField(max_length=50)
    pied_fort = models.CharField(max_length=1, choices=PIED_FORT_CHOICES, default="D")
    nombre_but = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.poste})"


class Entraineur(models.Model):
    """
    Modèle représentant un entraîneur d'équipe de football.

    :ivar id_En: Identifiant unique de l'entraîneur (clé primaire).
    :vartype id_En: int

    :ivar nom: Nom complet de l'entraîneur.
    :vartype nom: str

    :ivar experience: Années d'expérience de l'entraîneur.
    :vartype experience: int

    :ivar nationalite: Nationalité de l'entraîneur.
    :vartype nationalite: str
    """

    id_En = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Années d'expérience")
    nationalite = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Equipe(models.Model):
    """
    Modèle représentant une équipe de football.

    :ivar id_Eq: Identifiant unique de l'équipe (clé primaire).
    :vartype id_Eq: int

    :ivar nom: Nom de l'équipe.
    :vartype nom: str

    :ivar stade: Nom du stade de l'équipe.
    :vartype stade: str

    :ivar entraineur: Entraîneur associé à cette équipe (relation OneToOne).
    :vartype entraineur: Entraineur

    :ivar joueurs: Joueurs associés à cette équipe (relation ManyToMany).
    :vartype joueurs: QuerySet[Joueur]
    """

    id_Eq = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    stade = models.CharField(max_length=100)
    entraineur = models.OneToOneField(Entraineur, on_delete=models.CASCADE)
    joueurs = models.ManyToManyField(Joueur)

    def __str__(self):
        return self.nom
