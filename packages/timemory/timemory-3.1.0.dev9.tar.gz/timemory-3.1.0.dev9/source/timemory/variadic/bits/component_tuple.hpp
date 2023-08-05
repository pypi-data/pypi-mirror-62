// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

/** \file bits/component_tuple.hpp
 * \headerfile bits/component_tuple.hpp "timemory/variadic/bits/component_tuple.hpp"
 * Implementation for various functions
 *
 */

#pragma once

#include "timemory/manager.hpp"
#include "timemory/mpl/filters.hpp"
#include "timemory/variadic/generic_bundle.hpp"

//======================================================================================//
//
//      tim::get functions
//
namespace tim
{
//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline component_tuple<Types...>::component_tuple()
{
    if(settings::enabled())
        init_storage();
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
template <typename _Func>
inline component_tuple<Types...>::component_tuple(const string_t& key, const bool& store,
                                                  const bool& flat, const _Func& _func)
: bundle_type((settings::enabled()) ? add_hash_id(key) : 0, store, flat)
, m_data(data_type{})
{
    if(settings::enabled())
    {
        init_storage();
        _func(*this);
        set_object_prefix(key);
        apply_v::access<operation_t<operation::set_flat_profile>>(m_data, flat);
    }
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
template <typename _Func>
inline component_tuple<Types...>::component_tuple(const captured_location_t& loc,
                                                  const bool& store, const bool& flat,
                                                  const _Func& _func)
: bundle_type(loc.get_hash(), store, flat)
, m_data(data_type{})
{
    if(settings::enabled())
    {
        init_storage();
        _func(*this);
        set_object_prefix(loc.get_id());
        apply_v::access<operation_t<operation::set_flat_profile>>(m_data, flat);
    }
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline component_tuple<Types...>
component_tuple<Types...>::clone(bool store, bool flat)
{
    component_tuple tmp(*this);
    tmp.m_store = store;
    tmp.m_flat  = flat;
    return tmp;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
component_tuple<Types...>::~component_tuple()
{
    pop();
}

//--------------------------------------------------------------------------------------//
// insert into graph
//
template <typename... Types>
inline void
component_tuple<Types...>::push()
{
    if(m_store && !m_is_pushed)
    {
        // reset the data
        apply_v::access<operation_t<operation::reset>>(m_data);
        // avoid pushing/popping when already pushed/popped
        m_is_pushed = true;
        // insert node or find existing node
        apply_v::access<operation_t<operation::insert_node>>(m_data, m_hash, m_flat);
    }
}

//--------------------------------------------------------------------------------------//
// pop out of graph
//
template <typename... Types>
inline void
component_tuple<Types...>::pop()
{
    if(m_store && m_is_pushed)
    {
        // set the current node to the parent node
        apply_v::access<operation_t<operation::pop_node>>(m_data);
        // avoid pushing/popping when already pushed/popped
        m_is_pushed = false;
    }
}

//--------------------------------------------------------------------------------------//
// measure functions
//
template <typename... Types>
inline void
component_tuple<Types...>::measure()
{
    apply_v::access<operation_t<operation::measure>>(m_data);
}

//--------------------------------------------------------------------------------------//
// sample functions
//
template <typename... Types>
void
component_tuple<Types...>::sample()
{
    sample_type _samples{};
    apply_v::access2<operation_t<operation::sample>>(m_data, _samples);
}

//--------------------------------------------------------------------------------------//
// start/stop functions
//
template <typename... Types>
inline void
component_tuple<Types...>::start()
{
    using standard_start_t = operation_t<operation::standard_start>;

    using priority_types_t = impl::filter_false<negative_start_priority, impl_type>;
    using priority_tuple_t = mpl::sort<trait::start_priority, priority_types_t>;
    using priority_start_t = operation_t<operation::priority_start, priority_tuple_t>;

    using delayed_types_t = impl::filter_false<positive_start_priority, impl_type>;
    using delayed_tuple_t = mpl::sort<trait::start_priority, delayed_types_t>;
    using delayed_start_t = operation_t<operation::delayed_start, delayed_tuple_t>;

    // push components into the call-stack
    push();

    // increment laps
    ++m_laps;

    // start components
    apply_v::out_of_order<priority_start_t>(m_data);
    apply_v::access<standard_start_t>(m_data);
    apply_v::out_of_order<delayed_start_t>(m_data);
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline void
component_tuple<Types...>::stop()
{
    using standard_stop_t = operation_t<operation::standard_stop>;

    using priority_types_t = impl::filter_false<negative_stop_priority, impl_type>;
    using priority_tuple_t = mpl::sort<trait::stop_priority, priority_types_t>;
    using priority_stop_t  = operation_t<operation::priority_stop, priority_tuple_t>;

    using delayed_types_t = impl::filter_false<positive_stop_priority, impl_type>;
    using delayed_tuple_t = mpl::sort<trait::stop_priority, delayed_types_t>;
    using delayed_stop_t  = operation_t<operation::delayed_stop, delayed_tuple_t>;

    // stop components
    apply_v::out_of_order<priority_stop_t>(m_data);
    apply_v::access<standard_stop_t>(m_data);
    apply_v::out_of_order<delayed_stop_t>(m_data);

    // pop components off of the call-stack stack
    pop();
}

//--------------------------------------------------------------------------------------//
// recording
//
template <typename... Types>
inline typename component_tuple<Types...>::this_type&
component_tuple<Types...>::record()
{
    ++m_laps;
    apply_v::access<operation_t<operation::record>>(m_data);
    return *this;
}

//--------------------------------------------------------------------------------------//
// reset data
//
template <typename... Types>
inline void
component_tuple<Types...>::reset()
{
    apply_v::access<operation_t<operation::reset>>(m_data);
    m_laps = 0;
}

//--------------------------------------------------------------------------------------//
// get data
//
template <typename... Types>
inline typename component_tuple<Types...>::data_value_type
component_tuple<Types...>::get() const
{
    data_value_type _ret_data;
    apply_v::access2<operation_t<operation::get_data>>(m_data, _ret_data);
    return _ret_data;
}

//--------------------------------------------------------------------------------------//
// reset data
//
template <typename... Types>
inline typename component_tuple<Types...>::data_label_type
component_tuple<Types...>::get_labeled() const
{
    data_label_type _ret_data;
    apply_v::access2<operation_t<operation::get_data>>(m_data, _ret_data);
    return _ret_data;
}

//--------------------------------------------------------------------------------------//
// this_type operators
//
template <typename... Types>
inline typename component_tuple<Types...>::this_type&
component_tuple<Types...>::operator-=(const this_type& rhs)
{
    apply_v::access2<operation_t<operation::minus>>(m_data, rhs.m_data);
    m_laps -= rhs.m_laps;
    return *this;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline typename component_tuple<Types...>::this_type&
component_tuple<Types...>::operator-=(this_type& rhs)
{
    apply_v::access2<operation_t<operation::minus>>(m_data, rhs.m_data);
    m_laps -= rhs.m_laps;
    return *this;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline typename component_tuple<Types...>::this_type&
component_tuple<Types...>::operator+=(const this_type& rhs)
{
    apply_v::access2<operation_t<operation::plus>>(m_data, rhs.m_data);
    m_laps += rhs.m_laps;
    return *this;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline typename component_tuple<Types...>::this_type&
component_tuple<Types...>::operator+=(this_type& rhs)
{
    apply_v::access2<operation_t<operation::plus>>(m_data, rhs.m_data);
    m_laps += rhs.m_laps;
    return *this;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline void
component_tuple<Types...>::print_storage()
{
    apply_v::type_access<operation::print_storage, data_type>();
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline typename component_tuple<Types...>::data_type&
component_tuple<Types...>::data()
{
    return m_data;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline const typename component_tuple<Types...>::data_type&
component_tuple<Types...>::data() const
{
    return m_data;
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline void
component_tuple<Types...>::set_object_prefix(const string_t& _key) const
{
    apply_v::access<operation_t<operation::set_prefix>>(m_data, _key);
}

//--------------------------------------------------------------------------------------//
//
template <typename... Types>
inline void
component_tuple<Types...>::init_storage()
{
    static thread_local bool _once = []() {
        apply_v::type_access<operation::init_storage, data_type>();
        return true;
    }();
    consume_parameters(_once);
}

//--------------------------------------------------------------------------------------//

}  // namespace tim
