<template id="communities_dashboard">
    <div>
        <CollapsibleFilters ref="collapsible_filters" @created="collapsible_component_mounted" label= "Filter">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community ID:</label>
                        <select class="form-control" v-model="filterCommunityId">
                            <option value="all">All</option>
                            <option v-for="community in communities_list" :value="community.community_id">{{community.community_id}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community Name:</label>
                        <select class="form-control" v-model="filterCommunityName">
                            <option value="All">All</option>
                            <option v-for="community in communities_list" :value="community.community_name">{{community.community_name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community Status:</label>
                        <select class="form-control" v-model="filterCommunityStatus">
                            <option value="All">All</option>
                            <option v-for="community in communities_list" :value="community.community_status">{{community.community_status}}</option>
                        </select>
                    </div>
                </div>
                <!-- <div class="col-md-3">
                    <div class="form-group">
                        <label for="">WA Conservation Status:</label>
                        <select class="form-control">
                            <option value="All">All</option>
                        </select>
                    </div>
                </div> -->
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Workflow Status:</label>
                        <select class="form-control">
                            <option value="All">All</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-control">
                            <option value="All">All</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-control">
                            <option value="All">All</option>
                        </select>
                    </div>
                </div>

                <div v-if="is_external" class="col-md-6">
                    <router-link  style="margin-top:25px;" class="btn btn-primary pull-right" :to="{ name: 'apply_proposal' }">New Application</router-link>
                </div>
            </div>
        </CollapsibleFilters>

        <div class="row">
        <div class="col-lg-12">
            <datatable
                    ref="communities_datatable"
                    :id="datatable_id"
                    :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers"
                />
        </div>
        </div>
    </div>
</template>
<script>
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
//require("babel-polyfill"); /* only one of 'import' or 'require' is necessary */
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'CommunitiesTable',
    props: {
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','referral','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
        group_type_name:{
            type: String,
            required: true
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'communities-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterCommunityId: null,
            filterCommunityName: null,
            filterCommunityStatus: null,

            //Filter list for Community select box
            communities_list: [],
            
            // filtering options
            external_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'Under Review'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            internal_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'With Assessor'},
                {value: 'on_hold', name: 'On Hold'},
                {value: 'with_qa_officer', name: 'With QA Officer'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_assessor_requirements', name: 'With Assessor (Requirements)'},
                {value: 'with_approver', name: 'With Approver'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            
            proposal_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch:{
        filterCommunityId: function(){
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
        },
        filterCommunityName: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
        },
        filterCommunityStatus: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function(){
            if((this.filterCommunityId === null || this.filterCommunityId === 'all') && 
                (this.filterCommunityName === null || this.filterCommunityName.toLowerCase() === 'all') && 
                (this.filterCommunityStatus === null || this.filterCommunityStatus.toLowerCase() === 'all')){
                return false
            } else {
                return true
            }
        },
        is_external: function(){
            return this.level == 'external';
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        is_referral: function(){
            return this.level == 'referral';
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['id','Number', 'Community Id' ,'Community Name', 'Community Status', 'Region', 'District','Workflow Status', 'Action']
            }
            if (this.is_internal){
                return ['id','Number', 'Community Id' ,'Community Name', 'Community Status', 'Region', 'District','Workflow Status', 'Action']
            }
        },
        column_id: function(){
            return {
                // 1. ID
                data: "id",
                orderable: false,
                searchable: false,
                visible: false,
                'render': function(data, type, full){
                    return full.id
                }
            }
        },
        column_number: function(){
            return {
                // 2. Number
                data: "id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.id
                },
                name: "id",
            }
        },
        column_community_id: function(){
            return {
                data: "community_id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.community_id
                },
                name: "community_id",
            }
        },
        column_community_name: function(){
            return {
                data: "community_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.community_name){
                        return full.community_name
                    }
                    // Should not reach here
                    return ''
                },
                name: "community_name",
            }
        },
        column_community_status: function(){
            return {
                data: "community_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.community_status){
                        return full.community_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "community_status",
            }
        },
        column_region: function(){
            return {
                data: "region",
                orderable: true,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    if(full.region){
                        return full.region;
                    }
                    // Should not reach here
                    return ''
                },
                name: "region",
            }
        },
        column_district: function(){
            return {
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function(data, type, full){
                    if (full.district){
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "district",
            }
        },
        column_workflow_status: function(){
            return {
                data: "community_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.processing_status){
                        return full.processing_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "community_status",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (!vm.is_external){
                        /*if(vm.check_assessor(full) && full.can_officer_process)*/
                        if(full.assessor_process){   
                                links +=  `<a href='/internal/species_communities/${full.id}'>Process</a><br/>`;    
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${full.id}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (full.can_user_edit) {
                            links +=  `<a href='/external/species_communities/${full.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-proposal='${full.id}'>Discard</a><br/>`;
                        }
                        else if (full.can_user_view) {
                            links +=  `<a href='/external/species_communities/${full.id}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/species_communities/${full.id}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []
            if(vm.is_external){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
                    vm.column_action,
                ]
                search = true
                buttons = [
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend: 'csv',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ]
            }

            return {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                responsive: true,
                serverSide: true,
                searching: search,
                ajax: {
                    "url": api_endpoints.communities_paginated_internal,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.filter_common_id = vm.filterCommonId;
                        d.filter_community_name = vm.filterCommunityName;
                        d.filter_community_status = vm.filterCommunityStatus;
                        d.is_internal = vm.is_internal;
                    }
                },
                dom: 'lBfrtip',
                //buttons:[ ],
                buttons: buttons,

                columns: columns,
                processing: true,
                initComplete: function() {
                },
            }
        }
    
    },
    methods:{
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },

        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.community_filter_dict).then((response) => {
                vm.communities_list= response.body;
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            },(error) => {
                console.log(error);
            })
            //console.log(vm.regions);
        },

        discardProposal:function (proposal_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_proposal(proposal_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.communities_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.communities_datatable.vmDataTable.on('click', 'a[data-discard-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-proposal');
                vm.discardProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.communities_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        fetchProfile: function(){
            let vm = this;
            Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body;
                vm.is_payment_admin=response.body.is_payment_admin;
                              
            },(error) => {
                console.log(error);
                
            })
        },

        check_assessor: function(proposal){
            let vm = this;
            if (proposal.assigned_officer)
                {
                    { if(proposal.assigned_officer== vm.profile.full_name)
                        return true;
                    else
                        return false;
                }
            }
            else{
                 var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id=vm.profile.id)
                });
                
                if (assessor.length > 0)
                    return true;
                else
                    return false;
              
            }
            
        },
    },


    mounted: function(){
        this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseSearch();
            vm.addEventListeners();
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
