from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import DPI
from .serializers import DPISerializer
from .serializers import DPIDetailSerializer
from .permissions import IsPatient , IsInfirmier , IsMedecin , IsMedecinOrInfirmier, IsAdministratif
from django.contrib.auth import get_user_model




@api_view(['POST'])
@permission_classes([IsAdministratif])
def creer_dpi(request):
    """
    Crée un nouveau DPI pour un patient. Le champ `patient_id` et le champ `medecin` (nom du médecin) doivent être inclus dans la requête.
    """
    if request.method == 'POST':
        data = request.data.copy()  # Copie des données pour les manipulations

        User = get_user_model()    

        # Rechercher le médecin par son nom
        medecin_nom = data.get('medecin_traitant')
        if medecin_nom:
            medecin = User.objects.filter(role='medecin', nom=medecin_nom).first()
            if not medecin:
                return Response(
                    {"detail": f"Le médecin '{medecin_nom}' n'existe pas ou n'est pas valide."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Ajouter l'ID du médecin dans les données à sauvegarder
            data['medecin_traitant'] = medecin.id

        # Sérialiser les données avec le médecin traitant inclus
        serializer = DPISerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsPatient])
def consulter_dpi(request):
    """
    Consulter le DPI de l'utilisateur connecté via le token d'authentification.
    Le token d'authentification permet d'identifier l'utilisateur connecté et de récupérer son DPI.
    """
    try:
        # Récupérer le DPI pour l'utilisateur connecté en utilisant son ID via le token (request.user.id)
        dpi = DPI.objects.prefetch_related(
            'soins',
            'consultations__ordonnances__ordonnance_has_medicaments__medicament',
            'consultations__bilans__analysebiologique_set'
        ).select_related('patient').get(patient_id=request.user.id)
    except DPI.DoesNotExist:
        # Si aucun DPI n'est trouvé pour l'utilisateur, retourner une erreur
        return Response({'detail': 'DPI non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialisation et renvoi des données détaillées du DPI
    serializer = DPIDetailSerializer(dpi)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsMedecinOrInfirmier])
def rechercher_dpi_par_nss(request, nss):
    """
    Rechercher un DPI par NSS avec tous les détails.
    Accessible uniquement aux infirmiers et médecins.
    """
    try:
        # Chercher le DPI en fonction du NSS
        dpi = DPI.objects.prefetch_related(
            'soins',
            'consultations__ordonnances__ordonnance_has_medicaments__medicament',
            'consultations__bilans__analysebiologique_set'
        ).select_related('patient').get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser et retourner les données détaillées du DPI
    serializer = DPIDetailSerializer(dpi)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsMedecinOrInfirmier])
def consulter_dpi_par_qr(request, qr_code):
    """
    Consulter le DPI d'un patient via un QR Code (QR Code supposé contenir le NSS).
    Accessible uniquement aux infirmiers et médecins.
    """
    try:
        # Chercher le DPI en fonction du QR code (supposé être un NSS)
        dpi = DPI.objects.prefetch_related(
            'soins',
            'consultations__ordonnances__ordonnance_has_medicaments__medicament',
            'consultations__bilans__analysebiologique_set'
        ).select_related('patient').get(nss=qr_code)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce QR code.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser et retourner les données détaillées du DPI
    serializer = DPIDetailSerializer(dpi)
    return Response(serializer.data)



@api_view(['PATCH'])
@permission_classes([IsMedecin])
def modifier_dpi(request, dpi_id):
    """
    Modifier un DPI existant avec l'ID spécifié. 
    Cette vue est accessible uniquement aux médecins.
    """
    try:
        # Récupérer l'objet DPI en fonction de l'ID
        dpi = DPI.objects.get(nss=dpi_id)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Sérialiser et mettre à jour les données du DPI
    serializer = DPISerializer(dpi, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsMedecin])
def supprimer_dpi(request, dpi_id):
    """
    Supprimer un DPI existant avec l'ID spécifié. 
    Cette vue est accessible uniquement aux médecins.
    """
    try:
        # Récupérer l'objet DPI en fonction de l'ID
        dpi = DPI.objects.get(nss=dpi_id)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Supprimer le DPI
    dpi.delete()
    return Response({'detail': 'DPI supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)
