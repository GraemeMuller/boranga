from random import randrange
from django.db.models import DateField
from django.test import TestCase

# Create your tests here.
from boranga.components.species_and_communities.models import Species, GroupType, ConservationStatus, ConservationList, \
    ConservationCategory, ConservationCriteria, Taxonomy, Community, SpeciesDocument, ConservationThreat, \
    ConservationPlan, Distribution, ConservationAttributes

def create_test_data():
    print('----------------------------------------------------')
    print('--------------ADDING TEST DATA----------------------')
    print('----------------------------------------------------')
    read_data_files()
    # create_species_fauna()
    # create_species_fauna_no_community()
    # create_species_flora()
    # create_species_flora_no_community()

def read_data_files():
    import csv
    first_row = True
    with open('/home/graeme/workspace/boranga/boranga/components/species_and_communities/tests/fauna.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if first_row:
                first_row = False
                continue
            create_species_fauna(row)


def create_species_fauna(fauna_row):

    conservation_list = ConservationList.objects.create(name=fauna_row[1])
    conservation_category = ConservationCategory.objects.create(name=fauna_row[0].split('.')[2])
    conservation_criteria = ConservationCriteria.objects.create(name=fauna_row[4])
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)

    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[1][0])

    taxon = fauna_row[6]
    taxon_id = fauna_row[5]
    family = fauna_row[6]
    genus = fauna_row[6]
    phylogenetic_group = fauna_row[6]
    name_authority = "WA Museum"
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,)

    fauna = Species.objects.create(common_name=fauna_row[7],
                                   group_type = group_type,
                                   scientific_name = fauna_row[6],
                                   conservation_status = conservation_status,
                                   region = randrange(500),
                                   district = randrange(100),
                                   image = "path/to/fauna.jpg",
                                   taxonomy = taxonomy

    )
    fauna.save()


    # community_name = "Graeme's House"
    # community_id = 17
    # community_status = "Safe"
    # region = 1
    # district = 1
    # conservation_status = "Priority"
    # community = Community.objects.create(community_name=community_name,
    #                                      community_id=community_id,
    #                                      community_status=community_status,
    #                                      region=region,
    #                                      district=district,)
    # community.species.add(cat)
    # community.save()

    species_id = fauna_row[5]
    category_id = fauna_row[5]
    status = fauna_row[4]
    document = "{}.pdf".format(fauna_row[5])
    document_description = "{}.pdf".format(fauna_row[5])
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(fauna)
    species_id = taxon_id
    threat_category_id = randrange(1000),
    threat_description = fauna_row[3]
    comment = "{} is fauna".format(fauna_row[8])
    document = "{}.pdf".format(fauna_row[5])
    source = "WA Museum"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()
    
    _type = "Regular"
    threat_category_id = randrange(10000)
    region_id = randrange(1000)
    district_id = randrange(100)
    comment = "{} is a fauna plan.".format(fauna_row[8])
    source = "WA Museum"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(fauna)
    conservation_plans.save()

    department_file_numbers = fauna_row[3]
    community_original_area = randrange(10000)
    community_original_area_accuracy = randrange(1000)
    number_of_occurrences = randrange(100)
    extent_of_occurrences = randrange(100)
    area_of_occupancy = randrange(100)
    number_of_iucn_locations = randrange(100)
    community_original_area_reference = fauna_row[7]
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=fauna)
    distribution.save()

    general_management_advice = "{} is a fauna gen management advice.".format(fauna_row[8])
    ecological_attributes = "{} is a fauna eco attribute.".format(fauna_row[8])
    biological_attributes = "{} is a fauna bio attribute.".format(fauna_row[8])
    specific_survey_advice = "{} is a fauna survey advice.".format(fauna_row[8])
    comments = "{} is a fauna comment.".format(fauna_row[8])
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=fauna)
    conservation_attributes.save()

def create_species_fauna_no_community():

    conservation_list = ConservationList.objects.create(name="ConservationListFauna_no_community")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategory_no_community")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteria_no_community")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)

    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[1][0])

    taxon = "Dog"
    taxon_id = 966
    previous_name = "K9"
    family = "Puppy"
    genus = "Pooch"
    phylogenetic_group = "PuppusDoggus"
    name_authority = "Vet"
    community_id = 19
    community_number = 20
    community_description = "West biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    dog = Species.objects.create(common_name="Doggy",
                                 group_type = group_type,
                                 scientific_name = "Doggus",
                                 name_currency = "Good",
                                 conservation_status = conservation_status,
                                 region = 1,
                                 district = 1,
                                 image = "path/to/dog.jog",
                                 processing_status = "LOLOL 1",
                                 taxonomy = taxonomy

    )

    species_id = dog.id
    category_id = 11
    status = "Priority"
    document = "cat_doc.pdf"
    document_description = "A document describing the endangered status of a dog."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(dog)
    species_document.save()
    species_id = dog.id
    threat_category_id = 1122
    threat_description = "Bark bark."
    comment = "Feed ne."
    document = "dog_threat_document.docx"
    source = "Public"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()
    _type = "Thing"
    threat_category_id = 1441
    region_id = 114
    district_id = 1114
    comment = "Making poos."
    source = "Public"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(dog)
    conservation_plans.save()

    department_file_numbers = "444"
    community_original_area = 1
    community_original_area_accuracy = 0.75
    number_of_occurrences = 6
    extent_of_occurrences = 3
    area_of_occupancy = 2
    number_of_iucn_locations = 500
    community_original_area_reference = "South West"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=dog)
    distribution.save()

    general_management_advice = "Give  food."
    ecological_attributes = "Hug them."
    biological_attributes = "Very barky."
    specific_survey_advice = "Cuddle."
    comments = "Good dog."
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=dog)
    conservation_attributes.save()

def create_species_flora():

    conservation_list = ConservationList.objects.create(name="ConservationListFlora")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategoryFlora")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteriaFlora")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)
   
    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[0][0])

    taxon = "Rose"
    taxon_id = 777
    previous_name = "N/A"
    family = "Rosa"
    genus = "Flower"
    phylogenetic_group = "RosusFlowerus"
    name_authority = "WA Museum"
    community_id = 12
    community_number = 19
    community_description = "North-west biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    rose = Species.objects.create(common_name="Rose",
                                  group_type = group_type,
                                  scientific_name = "RosusFlowerus",
                                  name_currency = "No Idea Flora",
                                  conservation_status = conservation_status,
                                  region = 2,
                                  district = 2,
                                  image = "path/to/rose.jog",
                                  processing_status = "Complete 2",
                                  taxonomy = taxonomy

    )



    community_name = "Garden"
    community_id = 22
    community_status = "Weed problem"
    region = 2
    district = 2
    conservation_status = "Endangered"
    community = Community.objects.create(community_name=community_name,
                                         community_id=community_id,
                                         community_status=community_status,
                                         region=region,
                                         district=district,)
    community.species.add(rose)
    community.save()

    species_id = rose.id
    category_id = 11
    status = "Priority"
    document = "rose_doc.pdf"
    document_description = "A document describing the endangered status of a rose."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(rose)
    species_document.save()
    species_id = rose.id
    threat_category_id = 2222
    threat_description = "Prickly"
    comment = "Blah blah"
    document = "rose_threat_document.docx"
    source = "Museum"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()

    _type = "Special"
    threat_category_id = 3333
    region_id = 22
    district_id = 33
    comment = "Smells nice"
    source = "Person"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(rose)
    conservation_plans.save()

    department_file_numbers = "666, 777, 888"
    community_original_area = 12
    community_original_area_accuracy = 2.5
    number_of_occurrences = 10
    extent_of_occurrences = 50
    area_of_occupancy = 200
    number_of_iucn_locations = 7
    community_original_area_reference = "North West"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=rose)
    distribution.save()

    general_management_advice = "Water them"
    ecological_attributes = "Pretty"
    biological_attributes = "Nice"
    specific_survey_advice = "Pick them"
    comments = "Pretty nice smelling flower"
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=rose)
    conservation_attributes.save()

def create_species_flora_no_community():

    conservation_list = ConservationList.objects.create(name="ConservationListFloraNoCom")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategoryFloraNoCom")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteriaFloraNoCom")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)
   
    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[0][0])

    taxon = "Tulip"
    taxon_id = 755
    previous_name = "N/A"
    family = "Ta"
    genus = "FlowerPlant"
    phylogenetic_group = "TupipusFlowerus"
    name_authority = "Herbarium"
    community_id = 12
    community_number = 19
    community_description = "Perth biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    tuli = Species.objects.create(common_name="Tulip",
                                  group_type = group_type,
                                  scientific_name = "TulipFlowerus",
                                  name_currency = "No Idea Tulip",
                                  conservation_status = conservation_status,
                                  region = 25,
                                  district = 29,
                                  image = "path/to/Tulip.jog",
                                  processing_status = "Complete Tulip",
                                  taxonomy = taxonomy

    )

    species_id = tuli.id
    category_id = 11
    status = "Priority"
    document = "rose_doc.pdf"
    document_description = "A document describing the endangered status of a rose."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(tuli)
    species_document.save()
    species_id = rose.id
    threat_category_id = 2222
    threat_description = "Nice"
    comment = "Blah Bam bam"
    document = "tulip_threat_document.docx"
    source = "Herbarium"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()

    _type = "Nice"
    threat_category_id = 33335
    region_id = 225
    district_id = 335
    comment = "Smells"
    source = "Goat"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(rose)
    conservation_plans.save()

    department_file_numbers = "0, 8, 5, 7"
    community_original_area = 129
    community_original_area_accuracy = 2.55
    number_of_occurrences = 105
    extent_of_occurrences = 505
    area_of_occupancy = 2005
    number_of_iucn_locations = 75
    community_original_area_reference = "North"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=tuli)
    distribution.save()

    general_management_advice = "Water"
    ecological_attributes = "Pretty"
    biological_attributes = "Nice"
    specific_survey_advice = "Pick "
    comments = "Nice smelling flower"
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=tuli)
    conservation_attributes.save()