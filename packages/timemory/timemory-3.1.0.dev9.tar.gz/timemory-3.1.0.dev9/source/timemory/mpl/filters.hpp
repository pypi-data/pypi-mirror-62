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

#pragma once

#include "timemory/components/types.hpp"
#include "timemory/mpl/type_traits.hpp"
#include "timemory/mpl/types.hpp"

#include <tuple>

namespace tim
{
namespace impl
{
//======================================================================================//
//
//      filter if predicate evaluates to false (result)
//
//======================================================================================//

template <bool>
struct filter_if_false_result
{
    template <typename T>
    using type = std::tuple<T>;

    template <template <typename...> class Operator, typename T, typename... Tail>
    using operation_type = std::tuple<Operator<T, Tail...>>;
};

//--------------------------------------------------------------------------------------//

template <>
struct filter_if_false_result<false>
{
    template <typename T>
    using type = std::tuple<>;

    template <template <typename...> class Operator, typename T, typename... Tail>
    using operation_type = std::tuple<>;
};

//======================================================================================//
//
//      filter if predicate evaluates to true (result)
//
//======================================================================================//

template <bool>
struct filter_if_true_result
{
    template <typename T>
    using type = std::tuple<T>;

    template <template <typename...> class Operator, typename T, typename... Tail>
    using operation_type = std::tuple<Operator<T, Tail...>>;
};

//--------------------------------------------------------------------------------------//

template <>
struct filter_if_true_result<true>
{
    template <typename T>
    using type = std::tuple<>;

    template <template <typename...> class Operator, typename T, typename... Tail>
    using operation_type = std::tuple<>;
};

//======================================================================================//
//
//      filter if predicate evaluates to false (operator)
//
//======================================================================================//

template <template <typename> class Predicate, typename Sequence>
struct filter_if_false;

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, typename... Ts>
struct filter_if_false<Predicate, std::tuple<Ts...>>
{
    using type = tuple_concat_t<
        typename filter_if_false_result<Predicate<Ts>::value>::template type<Ts>...>;
};

//--------------------------------------------------------------------------------------//
/*
template <template <typename> class Predicate, template <typename...> class Tuple,
          typename... Ts>
struct filter_if_false<Predicate, Tuple<Ts...>>
{
    using type = tuple_concat_t<
        typename filter_if_false_result<Predicate<Ts>::value>::template type<Ts>...>;
};
*/
//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, typename Sequence>
using filter_false = typename filter_if_false<Predicate, Sequence>::type;

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename... Ts>
struct operation_filter_if_false
{
    using type = tuple_concat_t<typename filter_if_false_result<
        Predicate<Ts>::value>::template operation_type<Operator, Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename... Ts>
struct operation_filter_if_false<Predicate, Operator, std::tuple<Ts...>>
{
    using type = tuple_concat_t<typename filter_if_false_result<
        Predicate<Ts>::value>::template operation_type<Operator, Ts>...>;
};

//--------------------------------------------------------------------------------------//
/*
template <template <typename> class Predicate, template <typename...> class Operator,
          template <typename...> class Tuple, typename... Ts>
struct operation_filter_if_false<Predicate, Operator, Tuple<Ts...>>
{
    using type = tuple_concat_t<typename filter_if_false_result<
        Predicate<Ts>::value>::template operation_type<Operator, Ts>...>;
};
*/
//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename... Ts>
struct operation_filter_if_false<Predicate, Operator, std::tuple<std::tuple<Ts...>>>
{
    using type = tuple_concat_t<typename filter_if_false_result<
        Predicate<Ts>::value>::template operation_type<Operator, Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename Sequence>
using operation_filter_false =
    typename operation_filter_if_false<Predicate, Operator, Sequence>::type;

//======================================================================================//
//
//      filter if predicate evaluates to true (operator)
//
//======================================================================================//

template <template <typename> class Predicate, typename... Ts>
struct filter_if_true
{
    using type = tuple_concat_t<
        typename filter_if_true_result<Predicate<Ts>::value>::template type<Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, typename... Ts>
struct filter_if_true<Predicate, std::tuple<Ts...>>
{
    using type = tuple_concat_t<
        typename filter_if_true_result<Predicate<Ts>::value>::template type<Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, typename... Ts>
struct filter_if_true<Predicate, std::tuple<std::tuple<Ts...>>>
{
    using type = tuple_concat_t<
        typename filter_if_true_result<Predicate<Ts>::value>::template type<Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, typename Sequence>
using filter_true = typename filter_if_true<Predicate, Sequence>::type;

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename Sequence>
struct operation_filter_if_true;

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename... Ts>
struct operation_filter_if_true<Predicate, Operator, std::tuple<Ts...>>
{
    using type = tuple_concat_t<typename filter_if_true_result<
        Predicate<Ts>::value>::template operation_type<Operator, Ts>...>;
};

//--------------------------------------------------------------------------------------//

template <template <typename> class Predicate, template <typename...> class Operator,
          typename Sequence>
using operation_filter_true =
    typename operation_filter_if_true<Predicate, Operator, Sequence>::type;

//======================================================================================//
//
//      get data tuple
//
//======================================================================================//

template <typename _Tp>
struct get_data_tuple_type
{
    using type = conditional_t<(std::is_fundamental<_Tp>::value), _Tp,
                               decltype(std::declval<_Tp>().get())>;
};
/*
template <typename _Tp>
struct get_data_tuple_type<std::tuple<_Tp>>
{
    using type = conditional_t<(std::is_fundamental<_Tp>::value), _Tp,
                               decltype(std::declval<_Tp>().get())>;
};

template <typename _Tp>
struct get_data_tuple_type<type_list<_Tp>>
{
    using type = conditional_t<(std::is_fundamental<_Tp>::value), _Tp,
                               decltype(std::declval<_Tp>().get())>;
};
*/
template <typename... _ImplTypes>
struct get_data_tuple
{
    using value_type = std::tuple<_ImplTypes...>;
    using label_type = std::tuple<std::tuple<std::string, _ImplTypes>...>;
};

template <typename... _ImplTypes>
struct get_data_tuple<std::tuple<_ImplTypes...>>
{
    using value_type = std::tuple<typename get_data_tuple_type<_ImplTypes>::type...>;
    using label_type = std::tuple<
        std::tuple<std::string, typename get_data_tuple_type<_ImplTypes>::type>...>;
};

template <typename... _ImplTypes>
struct get_data_tuple<type_list<_ImplTypes...>>
{
    using value_type = std::tuple<typename get_data_tuple_type<_ImplTypes>::type...>;
    using label_type = std::tuple<
        std::tuple<std::string, typename get_data_tuple_type<_ImplTypes>::type>...>;
};

//======================================================================================//
// check if type is in expansion
//
template <typename...>
struct is_one_of
{
    static constexpr bool value = false;
};

template <typename F, typename S, template <typename...> class _Tuple, typename... T>
struct is_one_of<F, S, _Tuple<T...>>
{
    static constexpr bool value =
        std::is_same<F, S>::value || is_one_of<F, _Tuple<T...>>::value;
};

template <typename F, typename S, template <typename...> class _Tuple, typename... T>
struct is_one_of<F, _Tuple<S, T...>>
{
    static constexpr bool value = is_one_of<F, S, _Tuple<T...>>::value;
};

//======================================================================================//
// check if any types are integral types
//
template <typename...>
struct is_one_of_integral
{
    static constexpr bool value = false;
};

template <typename T, template <typename...> class _Tuple, typename... Tail>
struct is_one_of_integral<_Tuple<T, Tail...>>
{
    static constexpr bool value =
        std::is_integral<T>::value || is_one_of_integral<_Tuple<Tail...>>::value;
};

//======================================================================================//

template <typename In, typename Out>
struct remove_duplicates;

template <typename Out>
struct remove_duplicates<type_list<>, Out>
{
    using type = Out;
};

template <typename In, typename... InTail, typename... Out>
struct remove_duplicates<type_list<In, InTail...>, type_list<Out...>>
{
    using type = conditional_t<
        !(is_one_of<In, type_list<Out...>>::value),
        typename remove_duplicates<type_list<InTail...>, type_list<Out..., In>>::type,
        typename remove_duplicates<type_list<InTail...>, type_list<Out...>>::type>;
};

//--------------------------------------------------------------------------------------//

template <typename In, typename Out>
struct unique;

template <template <typename...> class InTuple, typename... In,
          template <typename...> class OutTuple, typename... Out>
struct unique<InTuple<In...>, OutTuple<Out...>>
{
    using tuple_type = convert_t<InTuple<In...>, OutTuple<>>;
    using dupl_type  = typename remove_duplicates<tuple_type, OutTuple<>>::type;
    using type       = convert_t<dupl_type, InTuple<>>;
};

//======================================================================================//

template <template <typename> class _Prio, typename _Beg, typename _Tp, typename _End>
struct sortT;

//--------------------------------------------------------------------------------------//

template <template <typename> class _Prio, typename _Tuple, typename _Beg = type_list<>,
          typename _End = type_list<>>
using sort = typename sortT<_Prio, _Tuple, _Beg, _End>::type;

//--------------------------------------------------------------------------------------//
//  Initiate recursion (zeroth sort operation)
//
template <template <typename> class _Prio, typename _In, typename... _InT>
struct sortT<_Prio, type_list<_In, _InT...>, type_list<>, type_list<>>
{
    using type =
        typename sortT<_Prio, type_list<_InT...>, type_list<>, type_list<_In>>::type;
};

//--------------------------------------------------------------------------------------//
//  Initiate recursion (zeroth sort operation)
//
template <template <typename> class _Prio, typename _In, typename... _InT>
struct sortT<_Prio, type_list<type_list<_In, _InT...>>, type_list<>, type_list<>>
{
    using type =
        typename sortT<_Prio, type_list<_InT...>, type_list<>, type_list<_In>>::type;
};

//--------------------------------------------------------------------------------------//
//  Terminate recursion (last sort operation)
//
template <template <typename> class _Prio, typename... _BegT, typename... _EndT>
struct sortT<_Prio, type_list<>, type_list<_BegT...>, type_list<_EndT...>>
{
    using type = type_list<_BegT..., _EndT...>;
};

//--------------------------------------------------------------------------------------//
//  If no current end, transfer begin to end ()
//
template <template <typename> class _Prio, typename _In, typename... _InT,
          typename... _BegT>
struct sortT<_Prio, type_list<_In, _InT...>, type_list<_BegT...>, type_list<>>
{
    using type = typename sortT<_Prio, type_list<_In, _InT...>, type_list<>,
                                type_list<_BegT...>>::type;
};

//--------------------------------------------------------------------------------------//
//  Specialization for first sort operation
//
template <template <typename> class _Prio, typename _In, typename _Tp, typename... _InT>
struct sortT<_Prio, type_list<_In, _InT...>, type_list<>, type_list<_Tp>>
{
    static constexpr bool value = (_Prio<_In>::value < _Prio<_Tp>::value);

    using type = conditional_t<
        (value),
        typename sortT<_Prio, type_list<_InT...>, type_list<>, type_list<_In, _Tp>>::type,
        typename sortT<_Prio, type_list<_InT...>, type_list<>,
                       type_list<_Tp, _In>>::type>;
};

//--------------------------------------------------------------------------------------//
//  Specialization for second sort operation
//
template <template <typename> class _Prio, typename _In, typename _Ta, typename _Tb,
          typename... _BegT, typename... _InT>
struct sortT<_Prio, type_list<_In, _InT...>, type_list<_BegT...>, type_list<_Ta, _Tb>>
{
    static constexpr bool iavalue = (_Prio<_In>::value < _Prio<_Ta>::value);
    static constexpr bool ibvalue = (_Prio<_In>::value < _Prio<_Tb>::value);
    static constexpr bool abvalue = (_Prio<_Ta>::value <= _Prio<_Tb>::value);

    using type = conditional_t<
        (iavalue),
        typename sortT<
            _Prio, type_list<_InT...>, sort<_Prio, type_list<_BegT..., _In>>,
            conditional_t<(abvalue), type_list<_Ta, _Tb>, type_list<_Tb, _Ta>>>::type,
        typename sortT<
            _Prio, type_list<_InT...>, sort<_Prio, type_list<_BegT..., _Ta>>,
            conditional_t<(ibvalue), type_list<_In, _Tb>, type_list<_Tb, _In>>>::type>;
};

//--------------------------------------------------------------------------------------//
//  Specialization for all other sort operations after first and second
//
template <template <typename> class _Prio, typename _In, typename _Tp, typename... _InT,
          typename... _BegT, typename... _EndT>
struct sortT<_Prio, type_list<_In, _InT...>, type_list<_BegT...>,
             type_list<_Tp, _EndT...>>
{
    static constexpr bool value = (_Prio<_In>::value < _Prio<_Tp>::value);

    using type = conditional_t<
        (value),
        typename sortT<_Prio, type_list<_InT...>, type_list<>,
                       type_list<_BegT..., _In, _Tp, _EndT...>>::type,
        typename sortT<_Prio, type_list<_In, _InT...>, type_list<_BegT..., _Tp>,
                       type_list<_EndT...>>::type>;
};

//======================================================================================//

}  // namespace impl

//======================================================================================//

///
///  generic alias for extracting all types with a specified trait enabled
///
template <template <typename> class Predicate, typename... Sequence>
struct get_true_types
{
    using type = impl::filter_false<Predicate, std::tuple<Sequence...>>;
};

template <template <typename> class Predicate, template <typename...> class Tuple,
          typename... Sequence>
struct get_true_types<Predicate, Tuple<Sequence...>>
{
    using type = impl::filter_false<Predicate, Tuple<Sequence...>>;
};

///
///  generic alias for extracting all types with a specified trait disabled
///
template <template <typename> class Predicate, typename... Sequence>
struct get_false_types
{
    using type = impl::filter_true<Predicate, std::tuple<Sequence...>>;
};

template <template <typename> class Predicate, template <typename...> class Tuple,
          typename... Sequence>
struct get_false_types<Predicate, Tuple<Sequence...>>
{
    using type = impl::filter_true<Predicate, Tuple<Sequence...>>;
};

//======================================================================================//

///
/// check if type is in expansion
///
template <typename _Tp, typename _Types>
using is_one_of = typename impl::is_one_of<_Tp, _Types>;

//======================================================================================//

///
/// check if type is in expansion
///
template <typename _Types>
using is_one_of_integral = typename impl::is_one_of_integral<_Types>;

//======================================================================================//

template <typename T>
using remove_duplicates = typename impl::unique<T, type_list<>>::type;

template <typename T>
using unique = typename impl::unique<T, type_list<>>::type;

//======================================================================================//
//
//      determines if storage should be implemented
//
//======================================================================================//

/// filter out any types that are not available
template <typename... Types>
using implemented = impl::filter_false<trait::is_available, std::tuple<Types...>>;

template <typename _Tuple>
using available_tuple = impl::filter_false<trait::is_available, _Tuple>;

/// filter out any operations on types that are not available
template <template <typename...> class Operator, typename... Types>
using modifiers =
    impl::operation_filter_false<trait::is_available, Operator, std::tuple<Types...>>;

//======================================================================================//
//
//      trait::num_gotchas
//
//======================================================================================//

/// filter out any types that are not available
template <typename... Types>
using filter_gotchas = impl::filter_false<trait::is_gotcha, std::tuple<Types...>>;

template <typename T>
using filter_gotchas_t = impl::filter_false<trait::is_gotcha, T>;

template <typename T>
using filter_empty_t = impl::filter_true<trait::is_empty, T>;

//======================================================================================//
//
//      {auto,component}_{hybrid,list,tuple} get() and get_labeled() types
//
//======================================================================================//

/// get the tuple of values
template <typename _Tuple>
using get_data_value_t = typename impl::template get_data_tuple<_Tuple>::value_type;

/// get the tuple of pair of descriptor and value
template <typename _Tuple>
using get_data_label_t = typename impl::template get_data_tuple<_Tuple>::label_type;

//======================================================================================//
//
//      sort
//
//======================================================================================//

namespace mpl
{
template <template <typename> class _Prio, typename _Tuple, typename _Beg = type_list<>,
          typename _End = type_list<>>
using sort = convert_t<typename impl::sortT<_Prio, convert_t<_Tuple, type_list<>>,
                                            convert_t<_Beg, type_list<>>,
                                            convert_t<_End, type_list<>>>::type,
                       std::tuple<>>;

}  // namespace mpl

template <typename _Tp, typename _Op>
struct negative_priority;

template <typename _Tp, typename _Op>
struct positive_priority;

template <typename _Tp, template <typename> class _Op>
struct negative_priority<_Tp, _Op<_Tp>>
{
    static constexpr bool value = (_Op<_Tp>::value < 0);
};

template <typename _Tp, template <typename> class _Op>
struct positive_priority<_Tp, _Op<_Tp>>
{
    static constexpr bool value = (_Op<_Tp>::value > 0);
};

template <typename _Tp>
struct negative_start_priority : negative_priority<_Tp, trait::start_priority<_Tp>>
{};

template <typename _Tp>
struct positive_start_priority : positive_priority<_Tp, trait::start_priority<_Tp>>
{};

template <typename _Tp>
struct negative_stop_priority : negative_priority<_Tp, trait::stop_priority<_Tp>>
{};

template <typename _Tp>
struct positive_stop_priority : positive_priority<_Tp, trait::stop_priority<_Tp>>
{};

}  // namespace tim
