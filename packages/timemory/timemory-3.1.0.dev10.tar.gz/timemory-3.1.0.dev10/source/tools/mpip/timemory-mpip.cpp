
#include "timemory/components/gotcha.hpp"
#include "timemory/library.h"
#include "timemory/timemory.hpp"

#include <memory>
#include <set>
#include <unordered_map>

using namespace tim::component;
using string_t      = std::string;
using stringset_t   = std::set<std::string>;
using mpi_toolset_t = tim::complete_list_t;
using mpip_gotcha_t = tim::component::gotcha<246, mpi_toolset_t>;
using mpip_tuple_t  = tim::component_tuple<mpip_gotcha_t>;
using toolset_ptr_t = std::shared_ptr<mpip_tuple_t>;
using record_map_t  = std::unordered_map<uint64_t, toolset_ptr_t>;

static toolset_ptr_t    _tool_instance;
static std::atomic<int> _tool_count;

extern "C"
{
    void create_record(const char* name, uint64_t* id, int, int*)
    {
        *id                                     = timemory_get_unique_id();
        auto obj                                = toolset_ptr_t(new mpip_tuple_t(name));
        timemory_tl_static<record_map_t>()[*id] = std::move(obj);
    }

    void delete_record(uint64_t nid)
    {
        auto& record_ids = timemory_tl_static<record_map_t>();
        // erase key from map which stops recording when object is destroyed
        record_ids.erase(nid);
    }

    uint64_t init_timemory_mpip_tools()
    {
        static bool is_initialized = false;
        if(!is_initialized)
        {
            // provide environment variable for enabling/disabling using custom record
            // types
            if(tim::get_env<bool>("ENABLE_TIMEMORY_MPIP_RECORD_TYPES", false))
            {
                timemory_create_function = (timemory_create_func_t) &create_record;
                timemory_delete_function = (timemory_delete_func_t) &delete_record;
            }

            // initialize manager
            auto manager = tim::manager::instance();
            tim::consume_parameters(manager);

            printf("[timemory]> %s...\n", __FUNCTION__);

            // activate gotcha without start/stop
            // mpip_gotcha_t::get_default_ready() = true;

            // generate the gotcha wrappers
            mpip_gotcha_t::get_initializer() = []() {
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 0, MPI_Accumulate);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 1, MPI_Add_error_class);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 2, MPI_Add_error_code);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 3, MPI_Add_error_string);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 4, MPI_Aint_add);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 5, MPI_Aint_diff);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 6, MPI_Allgather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 7, MPI_Allgatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 8, MPI_Alloc_mem);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 9, MPI_Allreduce);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 10, MPI_Alltoall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 11, MPI_Alltoallv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 12, MPI_Alltoallw);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 13, MPI_Barrier);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 14, MPI_Bcast);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 15, MPI_Bsend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 16, MPI_Bsend_init);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 17, MPI_Buffer_attach);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 18, MPI_Buffer_detach);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 19, MPI_Cancel);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 20, MPI_Cart_coords);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 21, MPI_Cart_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 22, MPI_Cart_get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 23, MPI_Cart_map);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 24, MPI_Cart_rank);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 25, MPI_Cart_shift);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 26, MPI_Cart_sub);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 27, MPI_Cartdim_get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 28, MPI_Close_port);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 29, MPI_Comm_accept);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 30, MPI_Comm_call_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 31, MPI_Comm_compare);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 32, MPI_Comm_connect);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 33, MPI_Comm_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 34, MPI_Comm_create_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 35, MPI_Comm_create_group);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 36, MPI_Comm_create_keyval);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 37, MPI_Comm_delete_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 38, MPI_Comm_disconnect);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 39, MPI_Comm_dup);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 40, MPI_Comm_dup_with_info);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 41, MPI_Comm_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 42, MPI_Comm_free_keyval);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 43, MPI_Comm_get_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 44, MPI_Comm_get_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 45, MPI_Comm_get_info);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 46, MPI_Comm_get_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 47, MPI_Comm_get_parent);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 48, MPI_Comm_group);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 49, MPI_Comm_idup);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 50, MPI_Comm_join);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 51, MPI_Comm_rank);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 52, MPI_Comm_remote_group);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 53, MPI_Comm_remote_size);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 54, MPI_Comm_set_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 55, MPI_Comm_set_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 56, MPI_Comm_set_info);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 57, MPI_Comm_set_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 58, MPI_Comm_size);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 59, MPI_Comm_spawn);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 60, MPI_Comm_spawn_multiple);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 61, MPI_Comm_split);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 62, MPI_Comm_split_type);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 63, MPI_Comm_test_inter);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 64, MPI_Compare_and_swap);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 65, MPI_Dims_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 66, MPI_Dist_graph_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 67, MPI_Dist_graph_create_adjacent);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 68, MPI_Dist_graph_neighbors);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 69, MPI_Dist_graph_neighbors_count);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 70, MPI_Error_class);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 71, MPI_Error_string);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 72, MPI_Exscan);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 73, MPI_Fetch_and_op);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 74, MPI_File_call_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 75, MPI_File_create_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 76, MPI_File_get_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 77, MPI_File_set_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 78, MPI_Free_mem);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 79, MPI_Gather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 80, MPI_Gatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 81, MPI_Get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 82, MPI_Get_accumulate);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 83, MPI_Get_address);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 84, MPI_Get_count);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 85, MPI_Get_elements);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 86, MPI_Get_elements_x);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 87, MPI_Get_library_version);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 88, MPI_Get_processor_name);
                // TIMEMORY_C_GOTCHA(mpip_gotcha_t, 89, MPI_Get_version);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 90, MPI_Graph_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 91, MPI_Graph_get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 92, MPI_Graph_map);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 93, MPI_Graph_neighbors);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 94, MPI_Graph_neighbors_count);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 95, MPI_Graphdims_get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 96, MPI_Grequest_complete);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 97, MPI_Grequest_start);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 98, MPI_Group_compare);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 99, MPI_Group_difference);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 100, MPI_Group_excl);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 101, MPI_Group_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 102, MPI_Group_incl);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 103, MPI_Group_intersection);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 104, MPI_Group_range_excl);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 105, MPI_Group_range_incl);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 106, MPI_Group_rank);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 107, MPI_Group_size);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 108, MPI_Group_translate_ranks);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 109, MPI_Group_union);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 110, MPI_Iallgather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 111, MPI_Iallgatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 112, MPI_Iallreduce);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 113, MPI_Ialltoall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 114, MPI_Ialltoallv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 115, MPI_Ialltoallw);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 116, MPI_Ibarrier);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 117, MPI_Ibcast);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 118, MPI_Ibsend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 119, MPI_Iexscan);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 120, MPI_Igather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 121, MPI_Igatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 122, MPI_Improbe);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 123, MPI_Imrecv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 124, MPI_Ineighbor_allgather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 125, MPI_Ineighbor_allgatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 126, MPI_Ineighbor_alltoall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 127, MPI_Ineighbor_alltoallv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 128, MPI_Ineighbor_alltoallw);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 129, MPI_Info_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 130, MPI_Info_delete);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 131, MPI_Info_dup);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 132, MPI_Info_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 133, MPI_Info_get);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 134, MPI_Info_get_nkeys);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 135, MPI_Info_get_nthkey);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 136, MPI_Info_get_valuelen);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 137, MPI_Info_set);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 138, MPI_Intercomm_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 139, MPI_Intercomm_merge);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 140, MPI_Iprobe);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 141, MPI_Irecv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 142, MPI_Ireduce);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 143, MPI_Ireduce_scatter);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 144, MPI_Ireduce_scatter_block);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 145, MPI_Irsend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 146, MPI_Is_thread_main);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 147, MPI_Iscan);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 148, MPI_Iscatter);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 149, MPI_Iscatterv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 150, MPI_Isend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 151, MPI_Issend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 152, MPI_Lookup_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 153, MPI_Mprobe);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 154, MPI_Mrecv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 155, MPI_Neighbor_allgather);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 156, MPI_Neighbor_allgatherv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 157, MPI_Neighbor_alltoall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 158, MPI_Neighbor_alltoallv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 159, MPI_Neighbor_alltoallw);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 160, MPI_Op_commutative);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 161, MPI_Op_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 162, MPI_Op_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 163, MPI_Open_port);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 164, MPI_Pack);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 165, MPI_Pack_external);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 166, MPI_Pack_external_size);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 167, MPI_Pack_size);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 168, MPI_Probe);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 169, MPI_Publish_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 170, MPI_Put);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 171, MPI_Query_thread);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 172, MPI_Raccumulate);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 173, MPI_Recv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 174, MPI_Recv_init);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 175, MPI_Reduce);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 176, MPI_Reduce_local);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 177, MPI_Reduce_scatter);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 178, MPI_Reduce_scatter_block);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 179, MPI_Request_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 180, MPI_Request_get_status);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 181, MPI_Rget);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 182, MPI_Rget_accumulate);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 183, MPI_Rput);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 184, MPI_Rsend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 185, MPI_Rsend_init);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 186, MPI_Scan);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 187, MPI_Scatter);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 188, MPI_Scatterv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 189, MPI_Send);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 190, MPI_Send_init);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 191, MPI_Sendrecv);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 192, MPI_Sendrecv_replace);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 193, MPI_Ssend);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 194, MPI_Ssend_init);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 195, MPI_Start);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 196, MPI_Startall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 197, MPI_Status_f2c);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 198, MPI_Status_set_cancelled);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 199, MPI_Status_set_elements);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 200, MPI_Status_set_elements_x);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 201, MPI_Topo_test);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 202, MPI_Unpack);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 203, MPI_Unpack_external);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 204, MPI_Unpublish_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 205, MPI_Wait);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 206, MPI_Waitall);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 207, MPI_Waitany);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 208, MPI_Waitsome);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 209, MPI_Win_allocate);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 210, MPI_Win_allocate_shared);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 211, MPI_Win_attach);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 212, MPI_Win_call_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 213, MPI_Win_complete);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 214, MPI_Win_create);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 215, MPI_Win_create_dynamic);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 216, MPI_Win_create_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 217, MPI_Win_create_keyval);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 218, MPI_Win_delete_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 219, MPI_Win_detach);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 220, MPI_Win_fence);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 221, MPI_Win_flush);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 222, MPI_Win_flush_all);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 223, MPI_Win_flush_local);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 224, MPI_Win_flush_local_all);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 225, MPI_Win_free);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 226, MPI_Win_free_keyval);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 227, MPI_Win_get_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 228, MPI_Win_get_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 229, MPI_Win_get_group);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 230, MPI_Win_get_info);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 231, MPI_Win_get_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 232, MPI_Win_lock);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 233, MPI_Win_lock_all);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 234, MPI_Win_post);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 235, MPI_Win_set_attr);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 236, MPI_Win_set_errhandler);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 237, MPI_Win_set_info);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 238, MPI_Win_set_name);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 239, MPI_Win_shared_query);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 240, MPI_Win_start);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 241, MPI_Win_sync);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 242, MPI_Win_test);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 243, MPI_Win_unlock);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 244, MPI_Win_unlock_all);
                TIMEMORY_C_GOTCHA(mpip_gotcha_t, 245, MPI_Win_wait);
            };

            // provide environment variable for suppressing wrappers
            mpip_gotcha_t::get_reject_list() = []() {
                auto reject_list =
                    tim::get_env<std::string>("TIMEMORY_MPIP_REJECT_LIST", "");
                if(reject_list.length() == 0)
                    return stringset_t{};
                auto        reject_list_vec = tim::delimit(reject_list);
                stringset_t reject_list_set;
                for(const auto& itr : reject_list_vec)
                    reject_list_set.insert(itr);
                return reject_list_set;
            };

            // provide environment variable for selecting wrappers
            mpip_gotcha_t::get_permit_list() = []() {
                auto permit_list =
                    tim::get_env<std::string>("TIMEMORY_MPIP_PERMIT_LIST", "");
                if(permit_list.length() == 0)
                    return stringset_t{};
                auto        permit_list_vec = tim::delimit(permit_list);
                stringset_t permit_list_set;
                for(const auto& itr : permit_list_vec)
                    permit_list_set.insert(itr);
                return permit_list_set;
            };

            is_initialized = true;
        }

        // provide environment variable for enabling/disabling
        if(tim::get_env<bool>("ENABLE_TIMEMORY_MPIP", true))
        {
            auto env_ret = tim::get_env<string_t>("TIMEMORY_PROFILER_COMPONENTS", "");
            if(env_ret.empty())
                env_ret = tim::get_env<string_t>("TIMEMORY_COMPONENT_LIST_INIT", "");
            auto env_enum = tim::enumerate_components(tim::delimit(env_ret));

            mpi_toolset_t::get_initializer() = [env_enum](mpi_toolset_t& cl) {
                ::tim::initialize(cl, env_enum);
            };

            if(!_tool_instance)
                _tool_instance = std::make_shared<mpip_tuple_t>("timemory_mpip");

            auto cleanup_functor = [=]() {
                if(_tool_instance)
                {
                    _tool_instance->stop();
                    _tool_instance.reset();
                }
            };
            auto idx = ++_tool_count;
            auto key = TIMEMORY_JOIN("-", "timemory-mpip", idx);
            tim::manager::instance()->add_cleanup(key, cleanup_functor);

            _tool_instance->start();
            return idx;
        }
        else
        {
            return 0;
        }
    }

    uint64_t stop_timemory_mpip_tools(uint64_t id)
    {
        if(id > 0 && _tool_instance.get())
        {
            auto key = TIMEMORY_JOIN("-", "timemory-mpip", id);
            auto idx = --_tool_count;
            tim::manager::instance()->remove_cleanup(key);
            _tool_instance->stop();
            if(idx == 0)
                _tool_instance.reset();
            return idx;
        }
        return 0;
    }

    uint64_t init_timemory_mpip_tools_() { return init_timemory_mpip_tools(); }
    uint64_t stop_timemory_mpip_tools_(uint64_t id)
    {
        return stop_timemory_mpip_tools(id);
    }

}  // extern "C"
