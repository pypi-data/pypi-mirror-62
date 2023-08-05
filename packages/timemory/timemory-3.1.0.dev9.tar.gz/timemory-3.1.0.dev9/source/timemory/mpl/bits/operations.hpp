//  MIT License
//
//  Copyright (c) 2020, The Regents of the University of California,
//  through Lawrence Berkeley National Laboratory (subject to receipt of any
//  required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.

/** \file mpl/bits/operations.hpp
 * \headerfile mpl/bits/operations.hpp "timemory/mpl/bits/operations.hpp"
 * These are some extra operations included in other place that add to the standard
 * mpl/operations but are separate so they can be included elsewhere to avoid
 * a cyclic include dependency
 *
 */

#pragma once

#include "timemory/components/base.hpp"
#include "timemory/components/types.hpp"
#include "timemory/data/statistics.hpp"
#include "timemory/mpl/stl_overload.hpp"
#include "timemory/mpl/type_traits.hpp"
#include "timemory/mpl/types.hpp"
#include "timemory/mpl/zip.hpp"
#include "timemory/settings.hpp"
#include "timemory/utility/serializer.hpp"

#include <array>
#include <bitset>
#include <iostream>
#include <ostream>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>

//======================================================================================//

namespace tim
{
//--------------------------------------------------------------------------------------//

namespace operation
{
//--------------------------------------------------------------------------------------//
/// \class common_utils
/// \brief common string manipulation utilities
///
struct common_utils
{
    using attributes_t   = std::map<string_t, string_t>;
    using strset_t       = std::set<string_t>;
    using stringstream_t = std::stringstream;
    using strvec_t       = std::vector<string_t>;

public:
    template <typename _Tp>
    static size_t get_distance(const _Tp& _data)
    {
        return get_distance_sfinae(_data);
    }

    template <typename _Tp>
    static auto get_distance_sfinae(const _Tp& _data, int)
        -> decltype(std::distance(_data.begin(), _data.end()), size_t())
    {
        return std::distance(_data.begin(), _data.end());
    }

    template <typename _Tp>
    static auto get_distance_sfinae(const _Tp&, long) -> size_t
    {
        return size_t(1);
    }

    template <typename _Tp>
    static auto get_distance_sfinae(const _Tp& _data)
        -> decltype(get_distance_sfinae(_data, 0))
    {
        return get_distance_sfinae(_data, 0);
    }

public:
    template <typename _Tp, enable_if_t<(std::is_arithmetic<_Tp>::value), int> = 0>
    static _Tp get_entry(const _Tp& _data, size_t)
    {
        return _data;
    }

    template <typename _Tp, enable_if_t<!(std::is_arithmetic<_Tp>::value), int> = 0>
    static auto get_entry(const _Tp& _data, size_t _idx)
        -> decltype(get_entry_sfinae_(_data, _idx))
    {
        return get_entry_sfinae_<_Tp>(_data, _idx);
    }

    template <typename _Tp, size_t _Idx>
    static _Tp get_entry(const _Tp& _data, size_t)
    {
        return _data;
    }

    template <typename _Tp>
    static auto get_entry_sfinae(const _Tp& _data, int, size_t _idx)
        -> decltype(_data.begin(), typename _Tp::value_type())
    {
        auto sz  = std::distance(_data.begin(), _data.end());
        auto n   = _idx % sz;
        auto itr = _data.begin();
        std::advance(itr, n);
        return *itr;
    }

    template <typename _Tp>
    static _Tp get_entry_sfinae(const _Tp& _data, long, size_t)
    {
        return _data;
    }

    template <typename _Tp>
    static auto get_entry_sfinae_(const _Tp& _data, size_t _idx)
        -> decltype(get_entry_sfinae(_data, 0, _idx))
    {
        return get_entry_sfinae<_Tp>(_data, 0, _idx);
    }

public:
    template <typename _Tp, typename _Wp, typename _Pp>
    static void write(std::vector<std::stringstream*>& _os,
                      std::ios_base::fmtflags _format, const _Tp& _data,
                      const _Wp& _width, const _Pp& _prec)
    {
        size_t num_data = get_distance(_data);

        for(size_t i = 0; i < num_data; ++i)
        {
            auto  _idata  = get_entry<_Tp>(_data, i);
            auto  _iwidth = get_entry<_Wp>(_width, i);
            auto  _iprec  = get_entry<_Pp>(_prec, i);
            auto* ss      = new std::stringstream;
            ss->setf(_format);
            (*ss) << std::setw(_iwidth) << std::setprecision(_iprec) << _idata;
            _os.emplace_back(ss);
        }
    }

    template <typename... _Tp, size_t... _Idx, typename _Wp, typename _Pp>
    static void write(std::vector<std::stringstream*>& _os,
                      std::ios_base::fmtflags _format, const std::tuple<_Tp...>& _data,
                      const _Wp& _width, const _Pp& _prec, index_sequence<_Idx...>)
    {
        using init_list_type = std::initializer_list<int>;
        auto&& ret           = init_list_type{ (
            write(_os, _format, std::get<_Idx>(_data), _width, _prec), 0)... };
        consume_parameters(ret);
    }

    template <typename... _Tp, typename _Wp, typename _Pp>
    static void write(std::vector<std::stringstream*>& _os,
                      std::ios_base::fmtflags _format, const std::tuple<_Tp...>& _data,
                      const _Wp& _width, const _Pp& _prec)
    {
        constexpr size_t _N = sizeof...(_Tp);
        write(_os, _format, _data, _width, _prec, make_index_sequence<_N>{});
    }

public:
    template <typename _Tp>
    static int64_t get_size(const _Tp& _data)
    {
        return get_labels_sfinae(_data, 0);
    }

    template <typename _Tp>
    static auto get_size_sfinae(const _Tp& _data, int)
        -> decltype(_data.label_array(), int64_t())
    {
        return _data.label_array().size();
    }

    template <typename _Tp>
    static auto get_size_sfinae(const _Tp&, long) -> int64_t
    {
        return 1;
    }

public:
    template <typename _Tp>
    static auto get_labels_sfinae(const _Tp& _data, int)
        -> decltype(_data.label_array(), strvec_t())
    {
        strvec_t _ret;
        for(const auto& itr : _data.label_array())
            _ret.push_back(itr);
        return _ret;
    }

    template <typename _Tp>
    static auto get_labels_sfinae(const _Tp&, long) -> strvec_t
    {
        return strvec_t{ _Tp::get_label() };
    }

    template <typename _Tp>
    static strvec_t get_labels(const _Tp& _data)
    {
        return get_labels_sfinae(_data, 0);
    }

public:
    template <typename T>
    static strvec_t as_string_vec(const T& _data)
    {
        return strvec_t{ _data };
    }

    template <typename _Tp>
    static std::string as_string(const _Tp& _obj)
    {
        std::stringstream ss;
        ss << _obj;
        return ss.str();
    }

    template <typename... T, size_t... _Idx>
    static strvec_t as_string_vec(const std::tuple<T...>& _obj, index_sequence<_Idx...>)
    {
        using init_list_type = std::initializer_list<std::string>;
        auto&& ret           = init_list_type{ (as_string(std::get<_Idx>(_obj)))... };
        return strvec_t(ret);
    }

    template <typename... T>
    static strvec_t as_string_vec(const std::tuple<T...>& _obj)
    {
        constexpr size_t _N = sizeof...(T);
        return as_string_vec(_obj, make_index_sequence<_N>{});
    }

public:
    template <typename _Tp>
    static auto get_display_units_sfinae(const _Tp& _data, int)
        -> decltype(_data.display_unit_array(), strvec_t())
    {
        strvec_t _ret;
        for(const auto& itr : _data.display_unit_array())
            _ret.push_back(itr);
        return _ret;
    }

    template <typename _Tp>
    static auto get_display_units_sfinae(const _Tp&, long) -> strvec_t
    {
        return as_string_vec(_Tp::get_display_unit());
    }

    template <typename _Tp>
    static strvec_t get_display_units(const _Tp& _data)
    {
        return get_display_units_sfinae(_data, 0);
    }

public:
    using sizevector_t = std::vector<size_t>;

    template <typename _Tp>
    static sizevector_t get_widths(const _Tp& _data)
    {
        return get_widths_sfinae(_data, 0);
    }

    template <typename _Tp>
    static auto get_widths_sfinae(const _Tp& _data, int)
        -> decltype(_data.width_array(), sizevector_t())
    {
        return _data.width_array();
    }

    template <typename _Tp>
    static auto get_widths_sfinae(const _Tp&, long) -> sizevector_t
    {
        return sizevector_t{ _Tp::get_width() };
    }

    //----------------------------------------------------------------------------------//
    /// generate an attribute
    ///
    static string_t attribute_string(const string_t& key, const string_t& item)
    {
        return apply<string_t>::join("", key, "=", "\"", item, "\"");
    }

    //----------------------------------------------------------------------------------//
    /// replace matching values in item with str
    ///
    static string_t replace(string_t& item, const string_t& str, const strset_t& values)
    {
        for(const auto& itr : values)
        {
            while(item.find(itr) != string_t::npos)
                item = item.replace(item.find(itr), itr.length(), str);
        }
        return item;
    }

    //----------------------------------------------------------------------------------//
    /// convert to lowercase
    ///
    static string_t lowercase(string_t _str)
    {
        for(auto& itr : _str)
            itr = tolower(itr);
        return _str;
    }

    //----------------------------------------------------------------------------------//
    /// convert to uppercase
    ///
    static string_t uppercase(string_t _str)
    {
        for(auto& itr : _str)
            itr = toupper(itr);
        return _str;
    }

    //----------------------------------------------------------------------------------//
    /// check if str contains any of the string items
    ///
    static bool contains(const string_t& str, const strset_t& items)
    {
        for(const auto& itr : items)
        {
            if(lowercase(str).find(itr) != string_t::npos)
                return true;
        }
        return false;
    }

    //----------------------------------------------------------------------------------//
    /// shorthand for apply<string_t>::join(...)
    ///
    template <typename... _Args>
    static string_t join(const std::string& _delim, _Args&&... _args)
    {
        return apply<string_t>::join(_delim, std::forward<_Args>(_args)...);
    }

    //----------------------------------------------------------------------------------//

    static bool is_empty(const std::string& obj) { return obj.empty(); }

    //----------------------------------------------------------------------------------//

    template <typename _Tp, typename... _Extra>
    static bool is_empty(const std::vector<_Tp, _Extra...>& obj)
    {
        for(const auto& itr : obj)
            if(!itr.empty())
                return false;
        return true;
    }

    //----------------------------------------------------------------------------------//

    template <template <typename...> class _Tuple, typename... _Tp>
    static bool is_empty(const _Tuple<_Tp...>& obj)
    {
        using init_list_type = std::initializer_list<int>;
        using input_type     = _Tuple<_Tp...>;

        constexpr size_t _N = sizeof...(_Tp);
        std::bitset<_N>  _bits;

        auto&& ret = init_list_type{ (
            _bits[index_of<_Tp, input_type>::value] =
                (std::get<index_of<_Tp, input_type>::value>(obj).empty()),
            0)... };
        consume_parameters(ret);
        return _bits.all();
    }

    //----------------------------------------------------------------------------------//

    template <bool _Enabled, typename _Arg, enable_if_t<(_Enabled == true), int> = 0>
    static void print_tag(std::ostream& os, const _Arg& _arg)
    {
        if(!is_empty(_arg))
            os << " " << _arg;
    }

    //----------------------------------------------------------------------------------//

    template <bool _Enabled, typename _Arg, enable_if_t<(_Enabled == false), int> = 0>
    static void print_tag(std::ostream&, const _Arg&)
    {}
};

//--------------------------------------------------------------------------------------//
/// \class base_printer
/// \brief invoked from the base class to provide default printing behavior
//
template <typename _Tp>
struct base_printer : public common_utils
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;
    using widths_t   = std::vector<int64_t>;

    explicit base_printer(std::ostream& _os, const Type& _obj)
    {
        auto _value = static_cast<const Type&>(_obj).get_display();
        auto _disp  = Type::get_display_unit();
        auto _label = Type::get_label();
        auto _prec  = Type::get_precision();
        auto _width = Type::get_width();
        auto _flags = Type::get_format_flags();

        std::stringstream ss_value;
        std::stringstream ss_extra;
        ss_value.setf(_flags);
        ss_value << std::setw(_width) << std::setprecision(_prec) << _value;

        // check traits to see if we should print
        constexpr bool units_print = !trait::custom_unit_printing<Type>::value;
        constexpr bool label_print = !trait::custom_label_printing<Type>::value;

        print_tag<units_print>(ss_extra, _disp);
        print_tag<label_print>(ss_extra, _label);

        _os << ss_value.str() << ss_extra.str();
    }
};

//--------------------------------------------------------------------------------------//
/// \class base_printer
/// \brief invoked from the base class to provide default printing behavior
//
template <typename _Tp>
struct print_statistics : public common_utils
{
public:
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;
    using widths_t   = std::vector<int64_t>;

public:
    template <typename _Up, typename _Vp>
    struct stats_enabled
    {
        static constexpr bool value =
            (trait::record_statistics<_Up>::value && !(std::is_same<_Vp, void>::value) &&
             !(std::is_same<_Vp, std::tuple<>>::value) &&
             !(std::is_same<_Vp, statistics<void>>::value) &&
             !(std::is_same<_Vp, statistics<std::tuple<>>>::value));
    };

public:
    template <typename _Self, template <typename> class _Sp, typename _Vp,
              typename _Up = _Tp, enable_if_t<(stats_enabled<_Up, _Vp>::value), int> = 0>
    print_statistics(const Type&, utility::stream& _os, const _Self&,
                     const _Sp<_Vp>& _stats, uint64_t)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        bool use_min    = get_env<bool>("TIMEMORY_PRINT_MIN", true);
        bool use_max    = get_env<bool>("TIMEMORY_PRINT_MIN", true);
        bool use_var    = get_env<bool>("TIMEMORY_PRINT_VARIANCE", false);
        bool use_stddev = get_env<bool>("TIMEMORY_PRINT_STDDEV", true);

        if(use_min)
            utility::write_entry(_os, "MIN", _stats.get_min());
        if(use_max)
            utility::write_entry(_os, "MAX", _stats.get_max());
        if(use_var)
            utility::write_entry(_os, "VAR", _stats.get_variance());
        if(use_stddev)
            utility::write_entry(_os, "STDDEV", _stats.get_stddev());
    }

    template <typename _Self, typename _Vp, typename _Up = _Tp,
              enable_if_t<!(stats_enabled<_Up, _Vp>::value), int> = 0>
    print_statistics(const Type&, utility::stream&, const _Self&, const _Vp&, uint64_t)
    {}

    template <typename _Self>
    print_statistics(const Type&, utility::stream&, const _Self&,
                     const statistics<std::tuple<>>&, uint64_t)
    {}

public:
    template <template <typename> class _Sp, typename _Vp, typename _Up = _Tp,
              enable_if_t<(stats_enabled<_Up, _Vp>::value), int> = 0>
    static void get_header(utility::stream& _os, const _Sp<_Vp>&)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        bool use_min    = get_env<bool>("TIMEMORY_PRINT_MIN", true);
        bool use_max    = get_env<bool>("TIMEMORY_PRINT_MIN", true);
        bool use_var    = get_env<bool>("TIMEMORY_PRINT_VARIANCE", false);
        bool use_stddev = get_env<bool>("TIMEMORY_PRINT_STDDEV", true);

        auto _flags = _Tp::get_format_flags();
        auto _width = _Tp::get_width();
        auto _prec  = _Tp::get_precision();

        if(use_min)
            utility::write_header(_os, "MIN", _flags, _width, _prec);
        if(use_max)
            utility::write_header(_os, "MAX", _flags, _width, _prec);
        if(use_var)
            utility::write_header(_os, "VAR", _flags, _width, _prec);
        if(use_stddev)
            utility::write_header(_os, "STDDEV", _flags, _width, _prec);
    }

    template <typename _Vp, typename _Up = _Tp,
              enable_if_t<!(stats_enabled<_Up, _Vp>::value), int> = 0>
    static void get_header(utility::stream&, _Vp&)
    {}

    static void get_header(utility::stream&, const statistics<std::tuple<>>&) {}
};

//--------------------------------------------------------------------------------------//

template <typename _Tp>
struct print_header : public common_utils
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;
    using widths_t   = std::vector<int64_t>;

    //----------------------------------------------------------------------------------//
    // only if components are available
    //
    template <typename _Stats, typename _Up = _Tp,
              enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print_header(const Type& _obj, utility::stream& _os, const _Stats& _stats)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        auto _labels = get_labels(_obj);
        // auto _display = get_display_units(_obj);
        // std::cout << "[" << demangle<_Tp>() << "]> labels: ";
        // for(const auto& itr : _labels)
        //    std::cout << "'" << itr << "' ";
        // std::cout << "\n";

        _os.set_prefix_begin();
        utility::write_header(_os, "LABEL");
        utility::write_header(_os, "COUNT");
        utility::write_header(_os, "DEPTH");
        _os.set_prefix_end();

        // auto _opzip = [](const std::string& _lhs, const std::string& _rhs) {
        //    return tim::apply<std::string>::join("", _lhs, " [", _rhs, "]");
        // };

        auto ios_fixed = std::ios_base::fixed;
        auto ios_dec   = std::ios_base::dec;
        auto ios_showp = std::ios_base::showpoint;
        auto f_self    = ios_fixed | ios_dec | ios_showp;
        int  w_self    = 8;
        int  p_self    = 1;
        auto f_value   = _Tp::get_format_flags();
        auto w_value   = _Tp::get_width();
        auto p_value   = _Tp::get_precision();

        utility::write_header(_os, "METRIC");
        utility::write_header(_os, "UNITS");
        if(trait::report_sum<Type>::value)
            utility::write_header(_os, "SUM", f_value, w_value, p_value);
        if(trait::report_mean<Type>::value)
            utility::write_header(_os, "MEAN", f_value, w_value, p_value);
        print_statistics<_Tp>::get_header(_os, _stats);
        utility::write_header(_os, "% SELF", f_self, w_self, p_self);

        _os.insert_break();
        if(_labels.size() > 0)
        {
            for(size_t i = 0; i < _labels.size() - 1; ++i)
            {
                utility::write_header(_os, "METRIC");
                utility::write_header(_os, "UNITS");
                if(trait::report_sum<Type>::value)
                    utility::write_header(_os, "SUM", f_value, w_value, p_value);
                if(trait::report_mean<Type>::value)
                    utility::write_header(_os, "MEAN", f_value, w_value, p_value);
                print_statistics<_Tp>::get_header(_os, _stats);
                utility::write_header(_os, "% SELF", f_self, w_self, p_self);
                _os.insert_break();
            }
        }
    }

    template <typename... _Args, typename _Up = _Tp,
              enable_if_t<!(is_enabled<_Up>::value), char> = 0>
    print_header(const Type&, utility::stream&, _Args&&...)
    {}
};

//--------------------------------------------------------------------------------------//

template <typename _Tp>
struct print
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;
    using widths_t   = std::vector<int64_t>;

    //----------------------------------------------------------------------------------//
    // only if components are available
    //
    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(const Type& _obj, std::ostream& _os, bool _endline = false)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        std::stringstream ss;
        ss << _obj;
        if(_endline)
            ss << '\n';
        _os << ss.str();
    }

    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(std::size_t _N, std::size_t _Ntot, const Type& _obj, std::ostream& _os,
          bool _endline)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        std::stringstream ss;
        ss << _obj;
        if(_N + 1 < _Ntot)
            ss << ", ";
        else if(_N + 1 == _Ntot && _endline)
            ss << '\n';
        _os << ss.str();
    }

    template <typename _Vp, typename _Stats, typename _Up = _Tp,
              enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(const Type& _obj, utility::stream& _os, const string_t& _prefix, int64_t _laps,
          int64_t _depth, const _Vp& _self, const _Stats& _stats)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        auto _labels = common_utils::get_labels(_obj);
        auto _units  = common_utils::get_display_units(_obj);

        utility::write_entry(_os, "LABEL", _prefix);
        utility::write_entry(_os, "COUNT", _laps);
        utility::write_entry(_os, "DEPTH", _depth);
        utility::write_entry(_os, "METRIC", _labels, true);
        utility::write_entry(_os, "UNITS", _units, true);
        if(trait::report_sum<Type>::value)
            utility::write_entry(_os, "SUM", _obj.get());
        if(trait::report_mean<Type>::value)
            utility::write_entry(_os, "MEAN", _obj.get() / _obj.get_laps());
        print_statistics<_Tp>(_obj, _os, _self, _stats, _laps);
        utility::write_entry(_os, "% SELF", _self);
    }

    //----------------------------------------------------------------------------------//
    // only if components are available -- pointers
    //
    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(const Type* _obj, std::ostream& _os, bool _endline = false)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        if(_obj)
            print(*_obj, _os, _endline);
    }

    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(std::size_t _N, std::size_t _Ntot, const Type* _obj, std::ostream& _os,
          bool _endline)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        if(_obj)
            print(_N, _Ntot, *_obj, _os, _endline);
    }

    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print(const Type* _obj, std::ostream& _os, const string_t& _prefix, int64_t _laps,
          int64_t _depth, const widths_t& _output_widths, bool _endline,
          const string_t& _suffix = "")
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        if(_obj)
            print(*_obj, _os, _prefix, _laps, _depth, _output_widths, _endline, _suffix);
    }

    //----------------------------------------------------------------------------------//
    // print nothing if component is not available
    //
    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(const Type&, std::ostream&, bool = false)
    {}

    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(std::size_t, std::size_t, const Type&, std::ostream&, bool)
    {}

    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(const Type&, std::ostream&, const string_t&, int64_t, int64_t, const widths_t&,
          bool, const string_t& = "")
    {}

    //----------------------------------------------------------------------------------//
    // print nothing if component is not available -- pointers
    //
    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(const Type*, std::ostream&, bool = false)
    {}

    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(std::size_t, std::size_t, const Type*, std::ostream&, bool)
    {}

    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print(const Type*, std::ostream&, const string_t&, int64_t, int64_t, const widths_t&,
          bool, const string_t& = "")
    {}
};

//--------------------------------------------------------------------------------------//

template <typename _Tp>
struct print_storage
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;

    //----------------------------------------------------------------------------------//
    // only if components are available
    //
    template <typename _Up = _Tp, enable_if_t<(is_enabled<_Up>::value), char> = 0>
    print_storage()
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        auto _storage = tim::storage<_Tp>::noninit_instance();
        if(_storage)
        {
            _storage->stack_clear();
            _storage->print();
        }
    }

    //----------------------------------------------------------------------------------//
    // print nothing if component is not available
    //
    template <typename _Up                                         = _Tp,
              enable_if_t<(is_enabled<_Up>::value == false), char> = 0>
    print_storage()
    {}
};

//--------------------------------------------------------------------------------------//
/// \class operation::add_secondary
/// \brief
/// component contains secondary data resembling the original data
/// but should be another node entry in the graph. These types
/// must provide a get_secondary() member function and that member function
/// must return a pair-wise iterable container, e.g. std::map, of types:
///     - std::string
///     - value_type
///
template <typename _Tp>
struct add_secondary
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;
    using string_t   = std::string;

    //----------------------------------------------------------------------------------//
    // if secondary data explicitly specified
    //
    template <typename Storage, typename Iterator, typename Up = Type,
              enable_if_t<(trait::secondary_data<Up>::value), int> = 0>
    add_secondary(Storage* _storage, Iterator _itr, const Up& _rhs)
    {
        if(!trait::runtime_enabled<_Tp>::get() || _storage == nullptr)
            return;

        using secondary_data_t = std::tuple<Iterator, const string_t&, value_type>;
        for(const auto& _data : _rhs.get_secondary())
            _storage->append(secondary_data_t{ _itr, _data.first, _data.second });
    }

    //----------------------------------------------------------------------------------//
    // check if secondary data implicitly specified
    //
    template <typename Storage, typename Iterator, typename Up = Type,
              enable_if_t<!(trait::secondary_data<Up>::value), int> = 0>
    add_secondary(Storage* _storage, Iterator _itr, const Up& _rhs)
    {
        add_secondary_sfinae(_storage, _itr, _rhs, 0);
    }

private:
    //----------------------------------------------------------------------------------//
    //  If the component has a set_prefix(const string_t&) member function
    //
    template <typename Storage, typename Iterator, typename Up = Type>
    auto add_secondary_sfinae(Storage* _storage, Iterator _itr, const Up& _rhs, int)
        -> decltype(_rhs.get_secondary(), void())
    {
        if(!trait::runtime_enabled<_Tp>::get() || _storage == nullptr)
            return;

        using secondary_data_t = std::tuple<Iterator, const string_t&, value_type>;
        for(const auto& _data : _rhs.get_secondary())
            _storage->append(secondary_data_t{ _itr, _data.first, _data.second });
    }

    //----------------------------------------------------------------------------------//
    //  If the component does not have a set_prefix(const string_t&) member function
    //
    template <typename Storage, typename Iterator, typename Up = Type>
    auto add_secondary_sfinae(Storage*, Iterator, const Up&, long)
        -> decltype(void(), void())
    {}
};

//--------------------------------------------------------------------------------------//
/// \class operation::add_statistics
/// \brief
///     Enabling statistics in timemory has three parts:
///     1. tim::trait::record_statistics must be set to true for component
///     2. tim::trait::statistics must set the data type of the statistics
///         - this is usually set to the data type returned from get()
///         - tuple<> is the default and will fully disable statistics unless changed
///
template <typename T>
struct add_statistics
{
    using Type   = T;
    using EmptyT = std::tuple<>;

    //----------------------------------------------------------------------------------//
    // helper struct
    //
    template <typename U, typename StatsT>
    struct enabled_statistics
    {
        static constexpr bool value =
            (trait::record_statistics<U>::value && !std::is_same<StatsT, EmptyT>::value);
    };

    //----------------------------------------------------------------------------------//
    // if statistics is enabled
    //
    template <typename StatsT, typename U = Type,
              enable_if_t<(enabled_statistics<U, StatsT>::value), int> = 0>
    add_statistics(const U& rhs, StatsT& stats)
    {
        // for type comparison
        using incoming_t = decay_t<typename StatsT::value_type>;
        using expected_t = decay_t<typename trait::statistics<U>::type>;
        // check the incomming stat type against declared stat type
        // but allow for permissive_statistics when there is an acceptable
        // implicit conversion
        static_assert((!trait::permissive_statistics<U>::value &&
                       std::is_same<incoming_t, expected_t>::value),
                      "add_statistics was passed a data type different than declared "
                      "trait::statistics type. To disable this error, e.g. permit "
                      "implicit conversion, set trait::permissive_statistics "
                      "to true_type for component");
        using stats_policy_type = policy::record_statistics<U>;
        stats_policy_type::apply(stats, rhs);
    }

    //----------------------------------------------------------------------------------//
    // if statistics is not enabled
    //
    template <typename StatsT, typename U,
              enable_if_t<!(enabled_statistics<U, StatsT>::value), int> = 0>
    add_statistics(const U&, StatsT&)
    {}
};

//--------------------------------------------------------------------------------------//
///
/// \class operation::echo_measurement
///
/// \brief This operation class echoes DartMeasurements for a CDash dashboard
///
template <typename _Tp>
struct echo_measurement<_Tp, false> : public common_utils
{
    template <typename... _Args>
    echo_measurement(_Args&&...)
    {}
};

template <typename _Tp>
struct echo_measurement<_Tp, true> : public common_utils
{
    using Type       = _Tp;
    using value_type = typename Type::value_type;
    using base_type  = typename Type::base_type;

    //----------------------------------------------------------------------------------//
    /// generate a name attribute
    ///
    template <typename... _Args>
    static string_t generate_name(const string_t& _prefix, string_t _unit,
                                  _Args&&... _args)
    {
        if(settings::dart_label())
        {
            return (_unit.length() > 0 && _unit != "%")
                       ? join("//", Type::get_label(), _unit)
                       : Type::get_label();
        }

        auto _extra = join("/", std::forward<_Args>(_args)...);
        auto _label = uppercase(Type::get_label());
        _unit       = replace(_unit, "", { " " });
        string_t _name =
            (_extra.length() > 0) ? join("//", _extra, _prefix) : join("//", _prefix);

        auto _ret = join("//", _label, _name);

        if(_ret.length() > 0 && _ret.at(_ret.length() - 1) == '/')
            _ret.erase(_ret.length() - 1);

        if(_unit.length() > 0 && _unit != "%")
            _ret += "//" + _unit;

        return _ret;
    }

    //------------------------------------------------------------------------------//
    //
    struct impl
    {
        template <typename _Tuple, typename... _Args, size_t... _Nt,
                  enable_if_t<(sizeof...(_Nt) == 0), char> = 0>
        static std::string name_generator(const string_t&, _Tuple, _Args&&...,
                                          index_sequence<_Nt...>)
        {
            return "";
        }

        template <typename _Tuple, typename... _Args, size_t _Idx, size_t... _Nt,
                  enable_if_t<(sizeof...(_Nt) == 0), char> = 0>
        static std::string name_generator(const string_t& _prefix, _Tuple _units,
                                          _Args&&... _args, index_sequence<_Idx, _Nt...>)
        {
            return generate_name(_prefix, std::get<_Idx>(_units),
                                 std::forward<_Args>(_args)...);
        }

        template <typename _Tuple, typename... _Args, size_t _Idx, size_t... _Nt,
                  enable_if_t<(sizeof...(_Nt) > 0), char> = 0>
        static std::string name_generator(const string_t& _prefix, _Tuple _units,
                                          _Args&&... _args, index_sequence<_Idx, _Nt...>)
        {
            return join(
                ",",
                name_generator<_Tuple>(_prefix, _units, std::forward<_Args>(_args)...,
                                       index_sequence<_Idx>{}),
                name_generator<_Tuple>(_prefix, _units, std::forward<_Args>(_args)...,
                                       index_sequence<_Nt...>{}));
        }
    };

    //----------------------------------------------------------------------------------//
    /// generate a name attribute
    ///
    template <typename _Tuple, typename... _Args>
    static string_t generate_name(const string_t& _prefix, _Tuple _unit, _Args&&... _args)
    {
        constexpr size_t _N = std::tuple_size<_Tuple>::value;
        return impl::template name_generator<_Tuple>(
            _prefix, _unit, std::forward<_Args>(_args)..., make_index_sequence<_N>{});
    }

    //----------------------------------------------------------------------------------//
    /// generate a name attribute
    ///
    template <typename _Type, typename... _Alloc, typename... _Args>
    static string_t generate_name(const string_t&               _prefix,
                                  std::vector<_Type, _Alloc...> _unit, _Args&&... _args)
    {
        string_t ret;
        for(auto& itr : _unit)
            return join(",", ret,
                        generate_name(_prefix, itr, std::forward<_Args>(_args)...));
        return ret;
    }

    //----------------------------------------------------------------------------------//
    /// generate a name attribute
    ///
    template <typename _Type, size_t _N, typename... _Args>
    static string_t generate_name(const string_t& _prefix, std::array<_Type, _N> _unit,
                                  _Args&&... _args)
    {
        string_t ret;
        for(auto& itr : _unit)
            return join(",", ret,
                        generate_name(_prefix, itr, std::forward<_Args>(_args)...));
        return ret;
    }

    //----------------------------------------------------------------------------------//
    /// generate a measurement tag
    ///
    template <typename _Vt>
    static void generate_measurement(std::ostream& os, const attributes_t& attributes,
                                     const _Vt& value)
    {
        os << "<DartMeasurement";
        os << " " << attribute_string("type", "numeric/double");
        for(const auto& itr : attributes)
            os << " " << attribute_string(itr.first, itr.second);
        os << ">" << std::setprecision(Type::get_precision()) << value
           << "</DartMeasurement>\n\n";
    }

    //----------------------------------------------------------------------------------//
    /// generate a measurement tag
    ///
    template <typename _Vt, typename... _Extra>
    static void generate_measurement(std::ostream& os, attributes_t attributes,
                                     const std::vector<_Vt, _Extra...>& value)
    {
        auto _default_name = attributes["name"];
        int  i             = 0;
        for(const auto& itr : value)
        {
            std::stringstream ss;
            ss << "INDEX_" << i++ << " ";
            attributes["name"] = ss.str() + _default_name;
            generate_measurement(os, attributes, itr);
        }
    }

    //----------------------------------------------------------------------------------//
    /// generate a measurement tag
    ///
    template <typename Lhs, typename Rhs, typename... _Extra>
    static void generate_measurement(std::ostream& os, attributes_t attributes,
                                     const std::pair<Lhs, Rhs>& value)
    {
        auto default_name = attributes["name"];
        auto set_name     = [&](int i) {
            std::stringstream ss;
            ss << "INDEX_" << i << " ";
            attributes["name"] = ss.str() + default_name;
        };

        set_name(0);
        generate_measurement(os, attributes, value.first);
        set_name(1);
        generate_measurement(os, attributes, value.second);
    }

    //----------------------------------------------------------------------------------//
    /// generate the prefix
    ///
    static string_t generate_prefix(const strvec_t& hierarchy)
    {
        if(settings::dart_label())
            return string_t("");

        string_t              ret_prefix = "";
        string_t              add_prefix = "";
        static const strset_t repl_chars = { "\t", "\n", "<", ">" };
        for(const auto& itr : hierarchy)
        {
            auto prefix = itr;
            prefix      = replace(prefix, "", { ">>>" });
            prefix      = replace(prefix, "", { "|_" });
            prefix      = replace(prefix, "_", repl_chars);
            prefix      = replace(prefix, "_", { "__" });
            if(prefix.length() > 0 && prefix.at(prefix.length() - 1) == '_')
                prefix.erase(prefix.length() - 1);
            ret_prefix += add_prefix + prefix;
        }
        return ret_prefix;
    }

    //----------------------------------------------------------------------------------//
    /// assumes type is not a iterable
    ///
    template <typename _Up = _Tp, typename _Vt = value_type,
              enable_if_t<(is_enabled<_Up>::value), char> = 0,
              enable_if_t<!(trait::array_serialization<_Up>::value ||
                            trait::iterable_measurement<_Up>::value),
                          int>                            = 0>
    echo_measurement(_Up& obj, const strvec_t& hierarchy)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        auto prefix = generate_prefix(hierarchy);
        auto _unit  = Type::get_display_unit();
        auto name   = generate_name(prefix, _unit);
        auto _data  = obj.get();

        attributes_t   attributes = { { "name", name } };
        stringstream_t ss;
        generate_measurement(ss, attributes, _data);
        std::cout << ss.str() << std::flush;
    }

    //----------------------------------------------------------------------------------//
    /// assumes type is iterable
    ///
    template <typename _Up = _Tp, typename _Vt = value_type,
              enable_if_t<(is_enabled<_Up>::value), char> = 0,
              enable_if_t<(trait::array_serialization<_Up>::value ||
                           trait::iterable_measurement<_Up>::value),
                          int>                            = 0>
    echo_measurement(_Up& obj, const strvec_t& hierarchy)
    {
        if(!trait::runtime_enabled<_Tp>::get())
            return;

        auto prefix = generate_prefix(hierarchy);
        auto _data  = obj.get();

        attributes_t   attributes = {};
        stringstream_t ss;

        uint64_t idx     = 0;
        auto     _labels = obj.label_array();
        auto     _dunits = obj.display_unit_array();
        for(auto& itr : _data)
        {
            string_t _extra = (idx < _labels.size()) ? _labels.at(idx) : "";
            string_t _dunit = (idx < _labels.size()) ? _dunits.at(idx) : "";
            ++idx;
            attributes["name"] = generate_name(prefix, _dunit, _extra);
            generate_measurement(ss, attributes, itr);
        }
        std::cout << ss.str() << std::flush;
    }

    template <typename... _Args, typename _Up = _Tp, typename _Vt = value_type,
              enable_if_t<!(is_enabled<_Up>::value), char> = 0>
    echo_measurement(_Up&, _Args&&...)
    {}
};

//--------------------------------------------------------------------------------------//

namespace finalize
{
//--------------------------------------------------------------------------------------//
//
template <typename Type>
get<Type, true>::get(storage_type& data, result_type& ret)
{
    //------------------------------------------------------------------------------//
    //
    //  Compute the node prefix
    //
    //------------------------------------------------------------------------------//
    auto _get_node_prefix = [&]() {
        if(!data.m_node_init)
            return std::string(">>> ");

        // prefix spacing
        static uint16_t width = 1;
        if(data.m_node_size > 9)
            width = std::max(width, (uint16_t)(log10(data.m_node_size) + 1));
        std::stringstream ss;
        ss.fill('0');
        ss << "|" << std::setw(width) << data.m_node_rank << ">>> ";
        return ss.str();
    };

    //------------------------------------------------------------------------------//
    //
    //  Compute the indentation
    //
    //------------------------------------------------------------------------------//
    // fix up the prefix based on the actual depth
    auto _compute_modified_prefix = [&](const graph_node& itr) {
        std::string _prefix      = data.get_prefix(itr);
        std::string _indent      = "";
        std::string _node_prefix = _get_node_prefix();

        int64_t _depth = itr.depth() - 1;
        if(_depth > 0)
        {
            for(int64_t ii = 0; ii < _depth - 1; ++ii)
                _indent += "  ";
            _indent += "|_";
        }

        return _node_prefix + _indent + _prefix;
    };

    // convert graph to a vector
    auto convert_graph = [&]() {
        result_type _list;
        {
            // the head node should always be ignored
            int64_t _min = std::numeric_limits<int64_t>::max();
            for(const auto& itr : data.graph())
                _min = std::min<int64_t>(_min, itr.depth());

            for(auto itr = data.graph().begin(); itr != data.graph().end(); ++itr)
            {
                if(itr->depth() > _min)
                {
                    auto _depth     = itr->depth() - (_min + 1);
                    auto _prefix    = _compute_modified_prefix(*itr);
                    auto _rolling   = itr->id();
                    auto _stats     = itr->stats();
                    auto _parent    = graph_type::parent(itr);
                    auto _hierarchy = hierarchy_type{};
                    if(_parent && _parent->depth() > _min)
                    {
                        while(_parent)
                        {
                            _hierarchy.push_back(_parent->id());
                            _rolling += _parent->id();
                            _parent = graph_type::parent(_parent);
                            if(!_parent || !(_parent->depth() > _min))
                                break;
                        }
                    }
                    if(_hierarchy.size() > 1)
                        std::reverse(_hierarchy.begin(), _hierarchy.end());
                    _hierarchy.push_back(itr->id());
                    auto&& _entry = result_node(itr->id(), itr->obj(), _prefix, _depth,
                                                _rolling, _hierarchy, _stats);
                    _list.push_back(_entry);
                }
            }
        }

        bool _thread_scope_only = trait::thread_scope_only<Type>::value;
        if(!settings::collapse_threads() || _thread_scope_only)
            return _list;

        result_type _combined;

        //--------------------------------------------------------------------------//
        //
        auto _equiv = [&](const result_node& _lhs, const result_node& _rhs) {
            return (std::get<0>(_lhs) == std::get<0>(_rhs) &&
                    std::get<2>(_lhs) == std::get<2>(_rhs) &&
                    std::get<3>(_lhs) == std::get<3>(_rhs) &&
                    std::get<4>(_lhs) == std::get<4>(_rhs));
        };

        //--------------------------------------------------------------------------//
        //
        auto _exists = [&](const result_node& _lhs) {
            for(auto itr = _combined.begin(); itr != _combined.end(); ++itr)
            {
                if(_equiv(_lhs, *itr))
                    return itr;
            }
            return _combined.end();
        };

        //--------------------------------------------------------------------------//
        //  collapse duplicates
        //
        for(const auto& itr : _list)
        {
            auto citr = _exists(itr);
            if(citr == _combined.end())
            {
                _combined.push_back(itr);
            }
            else
            {
                citr->data() += itr.data();
                citr->data().plus(itr.data());
                citr->stats() += itr.stats();
            }
        }
        return _combined;
    };

    ret = convert_graph();
}

//--------------------------------------------------------------------------------------//

template <typename Type>
mpi_get<Type, true>::mpi_get(storage_type& data, distrib_type& results)
{
#if !defined(TIMEMORY_USE_MPI)
    if(settings::debug())
        PRINT_HERE("%s", "timemory not using MPI");

    results = distrib_type(1, data.get());
#else
    if(settings::debug())
        PRINT_HERE("%s", "timemory using MPI");

    // not yet implemented
    // auto comm =
    //    (settings::mpi_output_per_node()) ? mpi::get_node_comm() : mpi::comm_world_v;
    auto comm = mpi::comm_world_v;
    mpi::barrier(comm);

    int mpi_rank = mpi::rank(comm);
    int mpi_size = mpi::size(comm);

    //------------------------------------------------------------------------------//
    //  Used to convert a result to a serialization
    //
    auto send_serialize = [&](const result_type& src) {
        std::stringstream ss;
        {
            auto oa = trait::output_archive<cereal::MinimalJSONOutputArchive>::get(ss);
            (*oa)(cereal::make_nvp("data", src));
        }
        return ss.str();
    };

    //------------------------------------------------------------------------------//
    //  Used to convert the serialization to a result
    //
    auto recv_serialize = [&](const std::string& src) {
        result_type       ret;
        std::stringstream ss;
        ss << src;
        {
            auto ia = trait::input_archive<cereal::MinimalJSONOutputArchive>::get(ss);
            (*ia)(cereal::make_nvp("data", ret));
            if(settings::debug())
                printf("[RECV: %i]> data size: %lli\n", mpi_rank,
                       (long long int) ret.size());
        }
        return ret;
    };

    results = distrib_type(mpi_size);

    auto ret     = data.get();
    auto str_ret = send_serialize(ret);

    if(mpi_rank == 0)
    {
        for(int i = 1; i < mpi_size; ++i)
        {
            std::string str;
            if(settings::debug())
                printf("[RECV: %i]> starting %i\n", mpi_rank, i);
            mpi::recv(str, i, 0, comm);
            if(settings::debug())
                printf("[RECV: %i]> completed %i\n", mpi_rank, i);
            results[i] = recv_serialize(str);
        }
        results[mpi_rank] = ret;
    }
    else
    {
        if(settings::debug())
            printf("[SEND: %i]> starting\n", mpi_rank);
        mpi::send(str_ret, 0, 0, comm);
        if(settings::debug())
            printf("[SEND: %i]> completed\n", mpi_rank);
        results = distrib_type(1, ret);
    }
#endif
}

//--------------------------------------------------------------------------------------//

template <typename Type>
upc_get<Type, true>::upc_get(storage_type& data, distrib_type& results)
{
#if !defined(TIMEMORY_USE_UPCXX)
    if(settings::debug())
        PRINT_HERE("%s", "timemory not using UPC++");

    results = distrib_type(1, data.get());
#else
    if(settings::debug())
        PRINT_HERE("%s", "timemory using UPC++");

    upc::barrier();

    int upc_rank = upc::rank();
    int upc_size = upc::size();

    //------------------------------------------------------------------------------//
    //  Used to convert a result to a serialization
    //
    auto send_serialize = [=](const result_type& src) {
        std::stringstream ss;
        {
            auto oa = trait::output_archive<cereal::MinimalJSONOutputArchive>::get(ss);
            (*oa)(cereal::make_nvp("data", src));
        }
        return ss.str();
    };

    //------------------------------------------------------------------------------//
    //  Used to convert the serialization to a result
    //
    auto recv_serialize = [=](const std::string& src) {
        result_type       ret;
        std::stringstream ss;
        ss << src;
        {
            auto ia = trait::input_archive<cereal::MinimalJSONOutputArchive>::get(ss);
            (*ia)(cereal::make_nvp("data", ret));
        }
        return ret;
    };

    //------------------------------------------------------------------------------//
    //  Function executed on remote node
    //
    auto remote_serialize = [=]() {
        return send_serialize(storage_type::master_instance()->get());
    };

    results.resize(upc_size);

    //------------------------------------------------------------------------------//
    //  Combine on master rank
    //
    if(upc_rank == 0)
    {
        for(int i = 1; i < upc_size; ++i)
        {
            upcxx::future<std::string> fut = upcxx::rpc(i, remote_serialize);
            while(!fut.ready())
                upcxx::progress();
            fut.wait();
            results[i] = recv_serialize(fut.result());
        }
        results[upc_rank] = data.get();
    }

    upcxx::barrier(upcxx::world());

    if(upc_rank != 0)
        results = distrib_type(1, data.get());
#endif
}

//--------------------------------------------------------------------------------------//
//
template <typename Type>
dmp_get<Type, true>::dmp_get(storage_type& data, distrib_type& results)
{
    auto fallback_get = [&]() { return distrib_type(1, data.get()); };

#if defined(TIMEMORY_USE_UPCXX) && defined(TIMEMORY_USE_MPI)
    results = (mpi::is_initialized())
                  ? data.mpi_get()
                  : ((upc::is_initialized()) ? data.upc_get() : fallback_get());
#elif defined(TIMEMORY_USE_UPCXX)
    results = (upc::is_initialized()) ? data.upc_get() : fallback_get();
#elif defined(TIMEMORY_USE_MPI)
    results = (mpi::is_initialized()) ? data.mpi_get() : fallback_get();
#else
    results = fallback_get();
#endif
}

}  // namespace finalize

//--------------------------------------------------------------------------------------//

}  // namespace operation

//--------------------------------------------------------------------------------------//

}  // namespace tim

//--------------------------------------------------------------------------------------//
