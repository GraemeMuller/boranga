import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
	GroupType,
	Species,
	Community,
	ConservationList,
	ConservationStatus,
	ConservationCategory,
	ConservationCriteria,
	Taxonomy,
	)

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q

logger = logging.getLogger('boranga')

class ListSpeciesSerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField()
	family = serializers.SerializerMethodField()
	genera = serializers.SerializerMethodField()
	phylogenetic_group = serializers.SerializerMethodField()
	conservation_status = serializers.SerializerMethodField()
	class Meta:
		model = Species
		fields = (
			    'id',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'taxonomy',
			    'family',
			    'genera',
			    'phylogenetic_group',
			    'region',
			    'district',
			    'conservation_status',
			    'processing_status',
			)
		datatables_always_serialize = (
                'id',
                'group_type',
			    'scientific_name',
			    'common_name',
			    'taxonomy',
			    'family',
			    'genera',
			    'phylogenetic_group',
			    'region',
			    'district',
			    'conservation_status',
			    'processing_status',
			)

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_family(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.family
		return None

	def get_genera(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.genus
		return None

	def get_phylogenetic_group(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.phylogenetic_group
		return None

	def get_conservation_status(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_list.name
		return None

class ListCommunitiesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Community
		fields = (
			    'id',
			    'community_id',
			    'community_name',
			    'community_status',
			    'region',
			    'district',
			)
		datatables_always_serialize = (
                'id',
			    'community_id',
			    'community_name',
			    'community_status',
			    'region',
			    'district',
			)