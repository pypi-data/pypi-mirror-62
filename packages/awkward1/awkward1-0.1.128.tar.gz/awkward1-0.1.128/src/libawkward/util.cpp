// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <cassert>
#include <sstream>
#include <set>

#include "rapidjson/document.h"

#include "awkward/cpu-kernels/identities.h"
#include "awkward/cpu-kernels/getitem.h"
#include "awkward/cpu-kernels/operations.h"
#include "awkward/cpu-kernels/reducers.h"

#include "awkward/util.h"
#include "awkward/Identities.h"

namespace rj = rapidjson;

namespace awkward {
  namespace util {
    void handle_error(const struct Error& err, const std::string& classname, const Identities* identities) {
      if (err.str != nullptr) {
        std::stringstream out;
        out << "in " << classname;
        if (err.identity != kSliceNone  &&  identities != nullptr) {
          assert(err.identity > 0);
          if (0 <= err.identity  &&  err.identity < identities->length()) {
            out << " with identity [" << identities->identity_at(err.identity) << "]";
          }
          else {
            out << " with invalid identity";
          }
        }
        if (err.attempt != kSliceNone) {
          out << " attempting to get " << err.attempt;
        }
        out << ", " << err.str;
        throw std::invalid_argument(out.str());
      }
    }

    template <typename T>
    IndexOf<T> make_starts(const IndexOf<T>& offsets) {
      return IndexOf<T>(offsets.ptr(), offsets.offset(), offsets.length() - 1);
    }

    template <typename T>
    IndexOf<T> make_stops(const IndexOf<T>& offsets) {
      return IndexOf<T>(offsets.ptr(), offsets.offset() + 1, offsets.length() - 1);
    }

    template IndexOf<int32_t> make_starts(const IndexOf<int32_t>& offsets);
    template IndexOf<uint32_t> make_starts(const IndexOf<uint32_t>& offsets);
    template IndexOf<int64_t> make_starts(const IndexOf<int64_t>& offsets);
    template IndexOf<int32_t> make_stops(const IndexOf<int32_t>& offsets);
    template IndexOf<uint32_t> make_stops(const IndexOf<uint32_t>& offsets);
    template IndexOf<int64_t> make_stops(const IndexOf<int64_t>& offsets);

    std::string quote(const std::string& x, bool doublequote) {
      // TODO: escape characters, possibly using RapidJSON.
      if (doublequote) {
        return std::string("\"") + x + std::string("\"");
      }
      else {
        return std::string("'") + x + std::string("'");
      }
    }

    std::shared_ptr<RecordLookup> init_recordlookup(int64_t numfields) {
      std::shared_ptr<RecordLookup> out = std::make_shared<RecordLookup>();
      for (int64_t i = 0;  i < numfields;  i++) {
        out.get()->push_back(std::to_string(i));
      }
      return out;
    }

    int64_t fieldindex(const std::shared_ptr<RecordLookup>& recordlookup, const std::string& key, int64_t numfields) {
      int64_t out = -1;
      if (recordlookup.get() != nullptr) {
        for (size_t i = 0;  i < recordlookup.get()->size();  i++) {
          if (recordlookup.get()->at(i) == key) {
            out = (int64_t)i;
            break;
          }
        }
      }
      if (out == -1) {
        try {
          out = (int64_t)std::stoi(key);
        }
        catch (std::invalid_argument err) {
          throw std::invalid_argument(std::string("key ") + quote(key, true) + std::string(" does not exist (not in record)"));
        }
        if (!(0 <= out  &&  out < numfields)) {
          throw std::invalid_argument(std::string("key interpreted as fieldindex ") + key + std::string(" for records with only " + std::to_string(numfields) + std::string(" fields")));
        }
      }
      return out;
    }

    const std::string key(const std::shared_ptr<RecordLookup>& recordlookup, int64_t fieldindex, int64_t numfields) {
      if (fieldindex >= numfields) {
        throw std::invalid_argument(std::string("fieldindex ") + std::to_string(fieldindex) + std::string(" for records with only " + std::to_string(numfields) + std::string(" fields")));
      }
      if (recordlookup.get() != nullptr) {
        return recordlookup.get()->at((size_t)fieldindex);
      }
      else {
        return std::to_string(fieldindex);
      }
    }

    bool haskey(const std::shared_ptr<RecordLookup>& recordlookup, const std::string& key, int64_t numfields) {
      try {
        fieldindex(recordlookup, key, numfields);
      }
      catch (std::invalid_argument err) {
        return false;
      }
      return true;
    }

    const std::vector<std::string> keys(const std::shared_ptr<RecordLookup>& recordlookup, int64_t numfields) {
      std::vector<std::string> out;
      if (recordlookup.get() != nullptr) {
        out.insert(out.end(), recordlookup.get()->begin(), recordlookup.get()->end());
      }
      else {
        int64_t cols = numfields;
        for (int64_t j = 0;  j < cols;  j++) {
          out.push_back(std::to_string(j));
        }
      }
      return out;
    }

    bool parameter_equals(const Parameters& parameters, const std::string& key, const std::string& value) {
      auto item = parameters.find(key);
      std::string myvalue;
      if (item == parameters.end()) {
        myvalue = "null";
      }
      else {
        myvalue = item->second;
      }
      rj::Document mine;
      rj::Document yours;
      mine.Parse<rj::kParseNanAndInfFlag>(myvalue.c_str());
      yours.Parse<rj::kParseNanAndInfFlag>(value.c_str());
      return mine == yours;
    }

    bool parameters_equal(const Parameters& self, const Parameters& other) {
      std::set<std::string> checked;
      for (auto pair : self) {
        if (!parameter_equals(other, pair.first, pair.second)) {
          return false;
        }
        checked.insert(pair.first);
      }
      for (auto pair : other) {
        if (checked.find(pair.first) == checked.end()) {
          if (!parameter_equals(self, pair.first, pair.second)) {
            return false;
          }
        }
      }
      return true;
    }

    template <>
    Error awkward_identities32_from_listoffsetarray<int32_t>(int32_t* toptr, const int32_t* fromptr, const int32_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listoffsetarray32(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_listoffsetarray<uint32_t>(int32_t* toptr, const int32_t* fromptr, const uint32_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listoffsetarrayU32(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_listoffsetarray<int64_t>(int32_t* toptr, const int32_t* fromptr, const int64_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listoffsetarray64(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listoffsetarray<int32_t>(int64_t* toptr, const int64_t* fromptr, const int32_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listoffsetarray32(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listoffsetarray<uint32_t>(int64_t* toptr, const int64_t* fromptr, const uint32_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listoffsetarrayU32(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listoffsetarray<int64_t>(int64_t* toptr, const int64_t* fromptr, const int64_t* fromoffsets, int64_t fromptroffset, int64_t offsetsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listoffsetarray64(toptr, fromptr, fromoffsets, fromptroffset, offsetsoffset, tolength, fromlength, fromwidth);
    }

    template <>
    Error awkward_identities32_from_listarray<int32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int32_t* fromstarts, const int32_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listarray32(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_listarray<uint32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listarrayU32(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_listarray<int64_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int64_t* fromstarts, const int64_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_listarray64(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listarray<int32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int32_t* fromstarts, const int32_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listarray32(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listarray<uint32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listarrayU32(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_listarray<int64_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int64_t* fromstarts, const int64_t* fromstops, int64_t fromptroffset, int64_t startsoffset, int64_t stopsoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_listarray64(uniquecontents, toptr, fromptr, fromstarts, fromstops, fromptroffset, startsoffset, stopsoffset, tolength, fromlength, fromwidth);
    }

    template <>
    Error awkward_identities32_from_indexedarray<int32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int32_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_indexedarray32(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_indexedarray<uint32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const uint32_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_indexedarrayU32(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities32_from_indexedarray<int64_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int64_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities32_from_indexedarray64(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_indexedarray<int32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int32_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_indexedarray32(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_indexedarray<uint32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const uint32_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_indexedarrayU32(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }
    template <>
    Error awkward_identities64_from_indexedarray<int64_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int64_t* fromindex, int64_t fromptroffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth) {
      return awkward_identities64_from_indexedarray64(uniquecontents, toptr, fromptr, fromindex, fromptroffset, indexoffset, tolength, fromlength, fromwidth);
    }

    template <>
    Error awkward_identities32_from_unionarray<int8_t, int32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int8_t* fromtags, const int32_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities32_from_unionarray8_32(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }
    template <>
    Error awkward_identities32_from_unionarray<int8_t, uint32_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int8_t* fromtags, const uint32_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities32_from_unionarray8_U32(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }
    template <>
    Error awkward_identities32_from_unionarray<int8_t, int64_t>(bool* uniquecontents, int32_t* toptr, const int32_t* fromptr, const int8_t* fromtags, const int64_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities32_from_unionarray8_64(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }
    template <>
    Error awkward_identities64_from_unionarray<int8_t, int32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int8_t* fromtags, const int32_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities64_from_unionarray8_32(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }
    template <>
    Error awkward_identities64_from_unionarray<int8_t, uint32_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int8_t* fromtags, const uint32_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities64_from_unionarray8_U32(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }
    template <>
    Error awkward_identities64_from_unionarray<int8_t, int64_t>(bool* uniquecontents, int64_t* toptr, const int64_t* fromptr, const int8_t* fromtags, const int64_t* fromindex, int64_t fromptroffset, int64_t tagsoffset, int64_t indexoffset, int64_t tolength, int64_t fromlength, int64_t fromwidth, int64_t which) {
      return awkward_identities64_from_unionarray8_64(uniquecontents, toptr, fromptr, fromtags, fromindex, fromptroffset, tagsoffset, indexoffset, tolength, fromlength, fromwidth, which);
    }

    template <>
    Error awkward_index_carry_64<int8_t>(int8_t* toindex, const int8_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t lenfromindex, int64_t length) {
      return awkward_index8_carry_64(toindex, fromindex, carry, fromindexoffset, lenfromindex, length);
    }
    template <>
    Error awkward_index_carry_64<uint8_t>(uint8_t* toindex, const uint8_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t lenfromindex, int64_t length) {
      return awkward_indexU8_carry_64(toindex, fromindex, carry, fromindexoffset, lenfromindex, length);
    }
    template <>
    Error awkward_index_carry_64<int32_t>(int32_t* toindex, const int32_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t lenfromindex, int64_t length) {
      return awkward_index32_carry_64(toindex, fromindex, carry, fromindexoffset, lenfromindex, length);
    }
    template <>
    Error awkward_index_carry_64<uint32_t>(uint32_t* toindex, const uint32_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t lenfromindex, int64_t length) {
      return awkward_indexU32_carry_64(toindex, fromindex, carry, fromindexoffset, lenfromindex, length);
    }
    template <>
    Error awkward_index_carry_64<int64_t>(int64_t* toindex, const int64_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t lenfromindex, int64_t length) {
      return awkward_index64_carry_64(toindex, fromindex, carry, fromindexoffset, lenfromindex, length);
    }

    template <>
    Error awkward_index_carry_nocheck_64<int8_t>(int8_t* toindex, const int8_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t length) {
      return awkward_index8_carry_nocheck_64(toindex, fromindex, carry, fromindexoffset, length);
    }
    template <>
    Error awkward_index_carry_nocheck_64<uint8_t>(uint8_t* toindex, const uint8_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t length) {
      return awkward_indexU8_carry_nocheck_64(toindex, fromindex, carry, fromindexoffset, length);
    }
    template <>
    Error awkward_index_carry_nocheck_64<int32_t>(int32_t* toindex, const int32_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t length) {
      return awkward_index32_carry_nocheck_64(toindex, fromindex, carry, fromindexoffset, length);
    }
    template <>
    Error awkward_index_carry_nocheck_64<uint32_t>(uint32_t* toindex, const uint32_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t length) {
      return awkward_indexU32_carry_nocheck_64(toindex, fromindex, carry, fromindexoffset, length);
    }
    template <>
    Error awkward_index_carry_nocheck_64<int64_t>(int64_t* toindex, const int64_t* fromindex, const int64_t* carry, int64_t fromindexoffset, int64_t length) {
      return awkward_index64_carry_nocheck_64(toindex, fromindex, carry, fromindexoffset, length);
    }

    template <>
    Error awkward_listarray_getitem_next_at_64<int32_t>(int64_t* tocarry, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t at) {
      return awkward_listarray32_getitem_next_at_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, at);
    }
    template <>
    Error awkward_listarray_getitem_next_at_64<uint32_t>(int64_t* tocarry, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t at) {
      return awkward_listarrayU32_getitem_next_at_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, at);
    }
    template <>
    Error awkward_listarray_getitem_next_at_64<int64_t>(int64_t* tocarry, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t at) {
      return awkward_listarray64_getitem_next_at_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, at);
    }

    template <>
    Error awkward_listarray_getitem_next_range_carrylength<int32_t>(int64_t* carrylength, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarray32_getitem_next_range_carrylength(carrylength, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }
    template <>
    Error awkward_listarray_getitem_next_range_carrylength<uint32_t>(int64_t* carrylength, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarrayU32_getitem_next_range_carrylength(carrylength, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }
    template <>
    Error awkward_listarray_getitem_next_range_carrylength<int64_t>(int64_t* carrylength, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarray64_getitem_next_range_carrylength(carrylength, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }

    template <>
    Error awkward_listarray_getitem_next_range_64<int32_t>(int32_t* tooffsets, int64_t* tocarry, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarray32_getitem_next_range_64(tooffsets, tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }
    template <>
    Error awkward_listarray_getitem_next_range_64<uint32_t>(uint32_t* tooffsets, int64_t* tocarry, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarrayU32_getitem_next_range_64(tooffsets, tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }
    template <>
    Error awkward_listarray_getitem_next_range_64<int64_t>(int64_t* tooffsets, int64_t* tocarry, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset, int64_t start, int64_t stop, int64_t step) {
      return awkward_listarray64_getitem_next_range_64(tooffsets, tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset, start, stop, step);
    }

    template <>
    Error awkward_listarray_getitem_next_range_counts_64<int32_t>(int64_t* total, const int32_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarray32_getitem_next_range_counts_64(total, fromoffsets, lenstarts);
    }
    template <>
    Error awkward_listarray_getitem_next_range_counts_64<uint32_t>(int64_t* total, const uint32_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarrayU32_getitem_next_range_counts_64(total, fromoffsets, lenstarts);
    }
    template <>
    Error awkward_listarray_getitem_next_range_counts_64<int64_t>(int64_t* total, const int64_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarray64_getitem_next_range_counts_64(total, fromoffsets, lenstarts);
    }

    template <>
    Error awkward_listarray_getitem_next_range_spreadadvanced_64<int32_t>(int64_t* toadvanced, const int64_t* fromadvanced, const int32_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarray32_getitem_next_range_spreadadvanced_64(toadvanced, fromadvanced, fromoffsets, lenstarts);
    }
    template <>
    Error awkward_listarray_getitem_next_range_spreadadvanced_64<uint32_t>(int64_t* toadvanced, const int64_t* fromadvanced, const uint32_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarrayU32_getitem_next_range_spreadadvanced_64(toadvanced, fromadvanced, fromoffsets, lenstarts);
    }
    template <>
    Error awkward_listarray_getitem_next_range_spreadadvanced_64<int64_t>(int64_t* toadvanced, const int64_t* fromadvanced, const int64_t* fromoffsets, int64_t lenstarts) {
      return awkward_listarray64_getitem_next_range_spreadadvanced_64(toadvanced, fromadvanced, fromoffsets, lenstarts);
    }

    template <>
    Error awkward_listarray_getitem_next_array_64<int32_t>(int64_t* tocarry, int64_t* toadvanced, const int32_t* fromstarts, const int32_t* fromstops, const int64_t* fromarray, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarray32_getitem_next_array_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }
    template <>
    Error awkward_listarray_getitem_next_array_64<uint32_t>(int64_t* tocarry, int64_t* toadvanced, const uint32_t* fromstarts, const uint32_t* fromstops, const int64_t* fromarray, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarrayU32_getitem_next_array_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }
    template <>
    Error awkward_listarray_getitem_next_array_64<int64_t>(int64_t* tocarry, int64_t* toadvanced, const int64_t* fromstarts, const int64_t* fromstops, const int64_t* fromarray, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarray64_getitem_next_array_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }

    template <>
    Error awkward_listarray_getitem_next_array_advanced_64<int32_t>(int64_t* tocarry, int64_t* toadvanced, const int32_t* fromstarts, const int32_t* fromstops, const int64_t* fromarray, const int64_t* fromadvanced, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarray32_getitem_next_array_advanced_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }
    template <>
    Error awkward_listarray_getitem_next_array_advanced_64<uint32_t>(int64_t* tocarry, int64_t* toadvanced, const uint32_t* fromstarts, const uint32_t* fromstops, const int64_t* fromarray, const int64_t* fromadvanced, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarrayU32_getitem_next_array_advanced_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }
    template <>
    Error awkward_listarray_getitem_next_array_advanced_64<int64_t>(int64_t* tocarry, int64_t* toadvanced, const int64_t* fromstarts, const int64_t* fromstops, const int64_t* fromarray, const int64_t* fromadvanced, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lenarray, int64_t lencontent) {
      return awkward_listarray64_getitem_next_array_advanced_64(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, startsoffset, stopsoffset, lenstarts, lenarray, lencontent);
    }

    template <>
    Error awkward_listarray_getitem_carry_64<int32_t>(int32_t* tostarts, int32_t* tostops, const int32_t* fromstarts, const int32_t* fromstops, const int64_t* fromcarry, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lencarry) {
      return awkward_listarray32_getitem_carry_64(tostarts, tostops, fromstarts, fromstops, fromcarry, startsoffset, stopsoffset, lenstarts, lencarry);
    }
    template <>
    Error awkward_listarray_getitem_carry_64<uint32_t>(uint32_t* tostarts, uint32_t* tostops, const uint32_t* fromstarts, const uint32_t* fromstops, const int64_t* fromcarry, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lencarry) {
      return awkward_listarrayU32_getitem_carry_64(tostarts, tostops, fromstarts, fromstops, fromcarry, startsoffset, stopsoffset, lenstarts, lencarry);
    }
    template <>
    Error awkward_listarray_getitem_carry_64<int64_t>(int64_t* tostarts, int64_t* tostops, const int64_t* fromstarts, const int64_t* fromstops, const int64_t* fromcarry, int64_t startsoffset, int64_t stopsoffset, int64_t lenstarts, int64_t lencarry) {
      return awkward_listarray64_getitem_carry_64(tostarts, tostops, fromstarts, fromstops, fromcarry, startsoffset, stopsoffset, lenstarts, lencarry);
    }

    template <>
    Error awkward_listarray_count<int32_t>(int32_t* tocount, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray32_count(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_count<uint32_t>(uint32_t* tocount, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarrayU32_count(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_count<int64_t>(int64_t* tocount, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray64_count(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }

    template <>
    Error awkward_listarray_count_64<int32_t>(int64_t* tocount, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray32_count_64(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_count_64<uint32_t>(int64_t* tocount, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarrayU32_count_64(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_count_64<int64_t>(int64_t* tocount, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray64_count_64(tocount, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }

    template <>
    Error awkward_listoffsetarray_count<int32_t>(int32_t* tocount, const int32_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarray32_count(tocount, fromoffsets, lenoffsets);
    }
    template <>
    Error awkward_listoffsetarray_count<uint32_t>(uint32_t* tocount, const uint32_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarrayU32_count(tocount, fromoffsets, lenoffsets);
    }
    template <>
    Error awkward_listoffsetarray_count<int64_t>(int64_t* tocount, const int64_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarray64_count(tocount, fromoffsets, lenoffsets);
    }

    template <>
    Error awkward_listoffsetarray_count_64<int32_t>(int64_t* tocount, const int32_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarray32_count_64(tocount, fromoffsets, lenoffsets);
    }
    template <>
    Error awkward_listoffsetarray_count_64<uint32_t>(int64_t* tocount, const uint32_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarrayU32_count_64(tocount, fromoffsets, lenoffsets);
    }
    template <>
    Error awkward_listoffsetarray_count_64<int64_t>(int64_t* tocount, const int64_t* fromoffsets, int64_t lenoffsets) {
      return awkward_listoffsetarray64_count_64(tocount, fromoffsets, lenoffsets);
    }

    template <>
    Error awkward_indexedarray_count<int32_t>(int64_t* tocount, const int64_t* contentcount, int64_t lencontent, const int32_t* fromindex, int64_t lenindex, int64_t indexoffset) {
      return awkward_indexedarray32_count(tocount, contentcount, lencontent, fromindex, lenindex, indexoffset);
    }
    template <>
    Error awkward_indexedarray_count<uint32_t>(int64_t* tocount, const int64_t* contentcount, int64_t lencontent, const uint32_t* fromindex, int64_t lenindex, int64_t indexoffset) {
      return awkward_indexedarrayU32_count(tocount, contentcount, lencontent, fromindex, lenindex, indexoffset);
    }
    template <>
    Error awkward_indexedarray_count<int64_t>(int64_t* tocount, const int64_t* contentcount, int64_t lencontent, const int64_t* fromindex, int64_t lenindex, int64_t indexoffset) {
      return awkward_indexedarray64_count(tocount, contentcount, lencontent, fromindex, lenindex, indexoffset);
    }

    template <>
    Error awkward_listarray_flatten_length<int32_t>(int64_t* tolen, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray32_flatten_length(tolen, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_length<uint32_t>(int64_t* tolen, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarrayU32_flatten_length(tolen, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_length<int64_t>(int64_t* tolen, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray64_flatten_length(tolen, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }

    template <>
    Error awkward_listarray_flatten_64<int32_t>(int64_t* tocarry, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray32_flatten_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_64<uint32_t>(int64_t* tocarry, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarrayU32_flatten_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_64<int64_t>(int64_t* tocarry, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray64_flatten_64(tocarry, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }

    template <>
    Error awkward_indexedarray_flatten_nextcarry_64<int32_t>(int64_t* tocarry, const int32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray32_flatten_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_flatten_nextcarry_64<uint32_t>(int64_t* tocarry, const uint32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarrayU32_flatten_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_flatten_nextcarry_64<int64_t>(int64_t* tocarry, const int64_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray64_flatten_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }

    template <>
    Error awkward_listarray_flatten_scale_64<int32_t>(int32_t* tostarts, int32_t* tostops, const int64_t* scale, const int32_t* fromstarts, const int32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray32_flatten_scale_64(tostarts, tostops, scale, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_scale_64<uint32_t>(uint32_t* tostarts, uint32_t* tostops, const int64_t* scale, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarrayU32_flatten_scale_64(tostarts, tostops, scale, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }
    template <>
    Error awkward_listarray_flatten_scale_64<int64_t>(int64_t* tostarts, int64_t* tostops, const int64_t* scale, const int64_t* fromstarts, const int64_t* fromstops, int64_t lenstarts, int64_t startsoffset, int64_t stopsoffset) {
      return awkward_listarray64_flatten_scale_64(tostarts, tostops, scale, fromstarts, fromstops, lenstarts, startsoffset, stopsoffset);
    }

    template <>
    Error awkward_indexedarray_numnull<int32_t>(int64_t* numnull, const int32_t* fromindex, int64_t indexoffset, int64_t lenindex) {
      return awkward_indexedarray32_numnull(numnull, fromindex, indexoffset, lenindex);
    }
    template <>
    Error awkward_indexedarray_numnull<uint32_t>(int64_t* numnull, const uint32_t* fromindex, int64_t indexoffset, int64_t lenindex) {
      return awkward_indexedarrayU32_numnull(numnull, fromindex, indexoffset, lenindex);
    }
    template <>
    Error awkward_indexedarray_numnull<int64_t>(int64_t* numnull, const int64_t* fromindex, int64_t indexoffset, int64_t lenindex) {
      return awkward_indexedarray64_numnull(numnull, fromindex, indexoffset, lenindex);
    }

    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_64<int32_t>(int64_t* tocarry, int32_t* toindex, const int32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray32_getitem_nextcarry_outindex_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_64<uint32_t>(int64_t* tocarry, uint32_t* toindex, const uint32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarrayU32_getitem_nextcarry_outindex_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_64<int64_t>(int64_t* tocarry, int64_t* toindex, const int64_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray64_getitem_nextcarry_outindex_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }

    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_mask_64<int32_t>(int64_t* tocarry, int64_t* toindex, const int32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray32_getitem_nextcarry_outindex_mask_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_mask_64<uint32_t>(int64_t* tocarry, int64_t* toindex, const uint32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarrayU32_getitem_nextcarry_outindex_mask_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_outindex_mask_64<int64_t>(int64_t* tocarry, int64_t* toindex, const int64_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray64_getitem_nextcarry_outindex_mask_64(tocarry, toindex, fromindex, indexoffset, lenindex, lencontent);
    }

    template <>
    Error awkward_indexedarray_getitem_nextcarry_64<int32_t>(int64_t* tocarry, const int32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray32_getitem_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_64<uint32_t>(int64_t* tocarry, const uint32_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarrayU32_getitem_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }
    template <>
    Error awkward_indexedarray_getitem_nextcarry_64<int64_t>(int64_t* tocarry, const int64_t* fromindex, int64_t indexoffset, int64_t lenindex, int64_t lencontent) {
      return awkward_indexedarray64_getitem_nextcarry_64(tocarry, fromindex, indexoffset, lenindex, lencontent);
    }

    template <>
    Error awkward_indexedarray_getitem_carry_64<int32_t>(int32_t* toindex, const int32_t* fromindex, const int64_t* fromcarry, int64_t indexoffset, int64_t lenindex, int64_t lencarry) {
      return awkward_indexedarray32_getitem_carry_64(toindex, fromindex, fromcarry, indexoffset, lenindex, lencarry);
    }
    template <>
    Error awkward_indexedarray_getitem_carry_64<uint32_t>(uint32_t* toindex, const uint32_t* fromindex, const int64_t* fromcarry, int64_t indexoffset, int64_t lenindex, int64_t lencarry) {
      return awkward_indexedarrayU32_getitem_carry_64(toindex, fromindex, fromcarry, indexoffset, lenindex, lencarry);
    }
    template <>
    Error awkward_indexedarray_getitem_carry_64<int64_t>(int64_t* toindex, const int64_t* fromindex, const int64_t* fromcarry, int64_t indexoffset, int64_t lenindex, int64_t lencarry) {
      return awkward_indexedarray64_getitem_carry_64(toindex, fromindex, fromcarry, indexoffset, lenindex, lencarry);
    }

    template <>
    Error awkward_indexedarray_overlay_mask8_to64<int32_t>(int64_t* toindex, const int8_t* mask, int64_t maskoffset, const int32_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarray32_overlay_mask8_to64(toindex, mask, maskoffset, fromindex, indexoffset, length);
    }
    template <>
    Error awkward_indexedarray_overlay_mask8_to64<uint32_t>(int64_t* toindex, const int8_t* mask, int64_t maskoffset, const uint32_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarrayU32_overlay_mask8_to64(toindex, mask, maskoffset, fromindex, indexoffset, length);
    }
    template <>
    Error awkward_indexedarray_overlay_mask8_to64<int64_t>(int64_t* toindex, const int8_t* mask, int64_t maskoffset, const int64_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarray64_overlay_mask8_to64(toindex, mask, maskoffset, fromindex, indexoffset, length);
    }

    template <>
    Error awkward_indexedarray_mask8<int32_t>(int8_t* tomask, const int32_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarray32_mask8(tomask, fromindex, indexoffset, length);
    }
    template <>
    Error awkward_indexedarray_mask8<uint32_t>(int8_t* tomask, const uint32_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarrayU32_mask8(tomask, fromindex, indexoffset, length);
    }
    template <>
    Error awkward_indexedarray_mask8<int64_t>(int8_t* tomask, const int64_t* fromindex, int64_t indexoffset, int64_t length) {
      return awkward_indexedarray64_mask8(tomask, fromindex, indexoffset, length);
    }

    template <>
    Error awkward_indexedarray_simplify32_to64<int32_t>(int64_t* toindex, const int32_t* outerindex, int64_t outeroffset, int64_t outerlength, const int32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray32_simplify32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplify32_to64<uint32_t>(int64_t* toindex, const uint32_t* outerindex, int64_t outeroffset, int64_t outerlength, const int32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarrayU32_simplify32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplify32_to64<int64_t>(int64_t* toindex, const int64_t* outerindex, int64_t outeroffset, int64_t outerlength, const int32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray64_simplify32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }

    template <>
    Error awkward_indexedarray_simplifyU32_to64<int32_t>(int64_t* toindex, const int32_t* outerindex, int64_t outeroffset, int64_t outerlength, const uint32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray32_simplifyU32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplifyU32_to64<uint32_t>(int64_t* toindex, const uint32_t* outerindex, int64_t outeroffset, int64_t outerlength, const uint32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarrayU32_simplifyU32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplifyU32_to64<int64_t>(int64_t* toindex, const int64_t* outerindex, int64_t outeroffset, int64_t outerlength, const uint32_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray64_simplifyU32_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }

    template <>
    Error awkward_indexedarray_simplify64_to64<int32_t>(int64_t* toindex, const int32_t* outerindex, int64_t outeroffset, int64_t outerlength, const int64_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray32_simplify64_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplify64_to64<uint32_t>(int64_t* toindex, const uint32_t* outerindex, int64_t outeroffset, int64_t outerlength, const int64_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarrayU32_simplify64_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }
    template <>
    Error awkward_indexedarray_simplify64_to64<int64_t>(int64_t* toindex, const int64_t* outerindex, int64_t outeroffset, int64_t outerlength, const int64_t* innerindex, int64_t inneroffset, int64_t innerlength) {
      return awkward_indexedarray64_simplify64_to64(toindex, outerindex, outeroffset, outerlength, innerindex, inneroffset, innerlength);
    }

    template <>
    Error awkward_unionarray_regular_index<int8_t, int32_t>(int32_t* toindex, const int8_t* fromtags, int64_t tagsoffset, int64_t length) {
      return awkward_unionarray8_32_regular_index(toindex, fromtags, tagsoffset, length);
    }
    template <>
    Error awkward_unionarray_regular_index<int8_t, uint32_t>(uint32_t* toindex, const int8_t* fromtags, int64_t tagsoffset, int64_t length) {
      return awkward_unionarray8_U32_regular_index(toindex, fromtags, tagsoffset, length);
    }
    template <>
    Error awkward_unionarray_regular_index<int8_t, int64_t>(int64_t* toindex, const int8_t* fromtags, int64_t tagsoffset, int64_t length) {
      return awkward_unionarray8_64_regular_index(toindex, fromtags, tagsoffset, length);
    }

    template <>
    Error awkward_unionarray_project_64<int8_t, int32_t>(int64_t* lenout, int64_t* tocarry, const int8_t* fromtags, int64_t tagsoffset, const int32_t* fromindex, int64_t indexoffset, int64_t length, int64_t which) {
      return awkward_unionarray8_32_project_64(lenout, tocarry, fromtags, tagsoffset, fromindex, indexoffset, length, which);
    }
    template <>
    Error awkward_unionarray_project_64<int8_t, uint32_t>(int64_t* lenout, int64_t* tocarry, const int8_t* fromtags, int64_t tagsoffset, const uint32_t* fromindex, int64_t indexoffset, int64_t length, int64_t which) {
      return awkward_unionarray8_U32_project_64(lenout, tocarry, fromtags, tagsoffset, fromindex, indexoffset, length, which);
    }
    template <>
    Error awkward_unionarray_project_64<int8_t, int64_t>(int64_t* lenout, int64_t* tocarry, const int8_t* fromtags, int64_t tagsoffset, const int64_t* fromindex, int64_t indexoffset, int64_t length, int64_t which) {
      return awkward_unionarray8_64_project_64(lenout, tocarry, fromtags, tagsoffset, fromindex, indexoffset, length, which);
    }

    template <>
    Error awkward_listarray_compact_offsets64(int64_t* tooffsets, const int32_t* fromstarts, const int32_t* fromstops, int64_t startsoffset, int64_t stopsoffset, int64_t length) {
      return awkward_listarray32_compact_offsets64(tooffsets, fromstarts, fromstops, startsoffset, stopsoffset, length);
    }
    template <>
    Error awkward_listarray_compact_offsets64(int64_t* tooffsets, const uint32_t* fromstarts, const uint32_t* fromstops, int64_t startsoffset, int64_t stopsoffset, int64_t length) {
      return awkward_listarrayU32_compact_offsets64(tooffsets, fromstarts, fromstops, startsoffset, stopsoffset, length);
    }
    template <>
    Error awkward_listarray_compact_offsets64(int64_t* tooffsets, const int64_t* fromstarts, const int64_t* fromstops, int64_t startsoffset, int64_t stopsoffset, int64_t length) {
      return awkward_listarray64_compact_offsets64(tooffsets, fromstarts, fromstops, startsoffset, stopsoffset, length);
    }

    template <>
    Error awkward_listoffsetarray_compact_offsets64(int64_t* tooffsets, const int32_t* fromoffsets, int64_t offsetsoffset, int64_t length) {
      return awkward_listoffsetarray32_compact_offsets64(tooffsets, fromoffsets, offsetsoffset, length);
    }
    template <>
    Error awkward_listoffsetarray_compact_offsets64(int64_t* tooffsets, const uint32_t* fromoffsets, int64_t offsetsoffset, int64_t length) {
      return awkward_listoffsetarrayU32_compact_offsets64(tooffsets, fromoffsets, offsetsoffset, length);
    }
    template <>
    Error awkward_listoffsetarray_compact_offsets64(int64_t* tooffsets, const int64_t* fromoffsets, int64_t offsetsoffset, int64_t length) {
      return awkward_listoffsetarray64_compact_offsets64(tooffsets, fromoffsets, offsetsoffset, length);
    }

    template <>
    Error awkward_listarray_broadcast_tooffsets64<int32_t>(int64_t* tocarry, const int64_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength, const int32_t* fromstarts, int64_t startsoffset, const int32_t* fromstops, int64_t stopsoffset, int64_t lencontent) {
      return awkward_listarray32_broadcast_tooffsets64(tocarry, fromoffsets, offsetsoffset, offsetslength, fromstarts, startsoffset, fromstops, stopsoffset, lencontent);
    }
    template <>
    Error awkward_listarray_broadcast_tooffsets64<uint32_t>(int64_t* tocarry, const int64_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength, const uint32_t* fromstarts, int64_t startsoffset, const uint32_t* fromstops, int64_t stopsoffset, int64_t lencontent) {
      return awkward_listarrayU32_broadcast_tooffsets64(tocarry, fromoffsets, offsetsoffset, offsetslength, fromstarts, startsoffset, fromstops, stopsoffset, lencontent);
    }
    template <>
    Error awkward_listarray_broadcast_tooffsets64<int64_t>(int64_t* tocarry, const int64_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength, const int64_t* fromstarts, int64_t startsoffset, const int64_t* fromstops, int64_t stopsoffset, int64_t lencontent) {
      return awkward_listarray64_broadcast_tooffsets64(tocarry, fromoffsets, offsetsoffset, offsetslength, fromstarts, startsoffset, fromstops, stopsoffset, lencontent);
    }

    template <>
    Error awkward_listoffsetarray_toRegularArray<int32_t>(int64_t* size, const int32_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength) {
      return awkward_listoffsetarray32_toRegularArray(size, fromoffsets, offsetsoffset, offsetslength);
    }
    template <>
    Error awkward_listoffsetarray_toRegularArray<uint32_t>(int64_t* size, const uint32_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength) {
      return awkward_listoffsetarrayU32_toRegularArray(size, fromoffsets, offsetsoffset, offsetslength);
    }
    template <>
    Error awkward_listoffsetarray_toRegularArray(int64_t* size, const int64_t* fromoffsets, int64_t offsetsoffset, int64_t offsetslength) {
      return awkward_listoffsetarray64_toRegularArray(size, fromoffsets, offsetsoffset, offsetslength);
    }

    template <>
    Error awkward_unionarray_simplify8_32_to8_64<int8_t, int32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_32_simplify8_32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_32_to8_64<int8_t, uint32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const uint32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_U32_simplify8_32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_32_to8_64<int8_t, int64_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int64_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_64_simplify8_32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }

    template <>
    Error awkward_unionarray_simplify8_U32_to8_64<int8_t, int32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const uint32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_32_simplify8_U32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_U32_to8_64<int8_t, uint32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const uint32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const uint32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_U32_simplify8_U32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_U32_to8_64<int8_t, int64_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int64_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const uint32_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_64_simplify8_U32_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }

    template <>
    Error awkward_unionarray_simplify8_64_to8_64<int8_t, int32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int64_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_32_simplify8_64_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_64_to8_64<int8_t, uint32_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const uint32_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int64_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_U32_simplify8_64_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify8_64_to8_64<int8_t, int64_t>(int8_t* totags, int64_t* toindex, const int8_t* outertags, int64_t outertagsoffset, const int64_t* outerindex, int64_t outerindexoffset, const int8_t* innertags, int64_t innertagsoffset, const int64_t* innerindex, int64_t innerindexoffset, int64_t towhich, int64_t innerwhich, int64_t outerwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_64_simplify8_64_to8_64(totags, toindex, outertags, outertagsoffset, outerindex, outerindexoffset, innertags, innertagsoffset, innerindex, innerindexoffset, towhich, innerwhich, outerwhich, length, base);
    }

    template <>
    Error awkward_unionarray_simplify_one_to8_64<int8_t, int32_t>(int8_t* totags, int64_t* toindex, const int8_t* fromtags, int64_t fromtagsoffset, const int32_t* fromindex, int64_t fromindexoffset, int64_t towhich, int64_t fromwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_32_simplify_one_to8_64(totags, toindex, fromtags, fromtagsoffset, fromindex, fromindexoffset, towhich, fromwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify_one_to8_64<int8_t, uint32_t>(int8_t* totags, int64_t* toindex, const int8_t* fromtags, int64_t fromtagsoffset, const uint32_t* fromindex, int64_t fromindexoffset, int64_t towhich, int64_t fromwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_U32_simplify_one_to8_64(totags, toindex, fromtags, fromtagsoffset, fromindex, fromindexoffset, towhich, fromwhich, length, base);
    }
    template <>
    Error awkward_unionarray_simplify_one_to8_64<int8_t, int64_t>(int8_t* totags, int64_t* toindex, const int8_t* fromtags, int64_t fromtagsoffset, const int64_t* fromindex, int64_t fromindexoffset, int64_t towhich, int64_t fromwhich, int64_t length, int64_t base) {
      return awkward_unionarray8_64_simplify_one_to8_64(totags, toindex, fromtags, fromtagsoffset, fromindex, fromindexoffset, towhich, fromwhich, length, base);
    }

    template <>
    Error awkward_listarray_getitem_jagged_expand_64<int32_t>(int64_t* multistarts, int64_t* multistops, const int64_t* singleoffsets, int64_t* tocarry, const int32_t* fromstarts, int64_t fromstartsoffset, const int32_t* fromstops, int64_t fromstopsoffset, int64_t jaggedsize, int64_t length) {
      return awkward_listarray32_getitem_jagged_expand_64(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, jaggedsize, length);
    }
    template <>
    Error awkward_listarray_getitem_jagged_expand_64(int64_t* multistarts, int64_t* multistops, const int64_t* singleoffsets, int64_t* tocarry, const uint32_t* fromstarts, int64_t fromstartsoffset, const uint32_t* fromstops, int64_t fromstopsoffset, int64_t jaggedsize, int64_t length) {
      return awkward_listarrayU32_getitem_jagged_expand_64(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, jaggedsize, length);
    }
    template <>
    Error awkward_listarray_getitem_jagged_expand_64(int64_t* multistarts, int64_t* multistops, const int64_t* singleoffsets, int64_t* tocarry, const int64_t* fromstarts, int64_t fromstartsoffset, const int64_t* fromstops, int64_t fromstopsoffset, int64_t jaggedsize, int64_t length) {
      return awkward_listarray64_getitem_jagged_expand_64(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, jaggedsize, length);
    }

    template <>
    Error awkward_listarray_getitem_jagged_apply_64<int32_t>(int64_t* tooffsets, int64_t* tocarry, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const int64_t* sliceindex, int64_t sliceindexoffset, int64_t sliceinnerlen, const int32_t* fromstarts, int64_t fromstartsoffset, const int32_t* fromstops, int64_t fromstopsoffset, int64_t contentlen) {
      return awkward_listarray32_getitem_jagged_apply_64(tooffsets, tocarry, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, sliceindex, sliceindexoffset, sliceinnerlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, contentlen);
    }
    template <>
    Error awkward_listarray_getitem_jagged_apply_64<uint32_t>(int64_t* tooffsets, int64_t* tocarry, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const int64_t* sliceindex, int64_t sliceindexoffset, int64_t sliceinnerlen, const uint32_t* fromstarts, int64_t fromstartsoffset, const uint32_t* fromstops, int64_t fromstopsoffset, int64_t contentlen) {
      return awkward_listarrayU32_getitem_jagged_apply_64(tooffsets, tocarry, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, sliceindex, sliceindexoffset, sliceinnerlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, contentlen);
    }
    template <>
    Error awkward_listarray_getitem_jagged_apply_64<int64_t>(int64_t* tooffsets, int64_t* tocarry, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const int64_t* sliceindex, int64_t sliceindexoffset, int64_t sliceinnerlen, const int64_t* fromstarts, int64_t fromstartsoffset, const int64_t* fromstops, int64_t fromstopsoffset, int64_t contentlen) {
      return awkward_listarray64_getitem_jagged_apply_64(tooffsets, tocarry, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, sliceindex, sliceindexoffset, sliceinnerlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset, contentlen);
    }

    template <>
    Error awkward_listarray_getitem_jagged_descend_64<int32_t>(int64_t* tooffsets, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const int32_t* fromstarts, int64_t fromstartsoffset, const int32_t* fromstops, int64_t fromstopsoffset) {
      return awkward_listarray32_getitem_jagged_descend_64(tooffsets, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset);
    }
    template <>
    Error awkward_listarray_getitem_jagged_descend_64<uint32_t>(int64_t* tooffsets, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const uint32_t* fromstarts, int64_t fromstartsoffset, const uint32_t* fromstops, int64_t fromstopsoffset) {
      return awkward_listarrayU32_getitem_jagged_descend_64(tooffsets, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset);
    }
    template <>
    Error awkward_listarray_getitem_jagged_descend_64<int64_t>(int64_t* tooffsets, const int64_t* slicestarts, int64_t slicestartsoffset, const int64_t* slicestops, int64_t slicestopsoffset, int64_t sliceouterlen, const int64_t* fromstarts, int64_t fromstartsoffset, const int64_t* fromstops, int64_t fromstopsoffset) {
      return awkward_listarray64_getitem_jagged_descend_64(tooffsets, slicestarts, slicestartsoffset, slicestops, slicestopsoffset, sliceouterlen, fromstarts, fromstartsoffset, fromstops, fromstopsoffset);
    }

    template <>
    Error awkward_indexedarray_reduce_next_64<int32_t>(int64_t* nextcarry, int64_t* nextparents, const int32_t* index, int64_t indexoffset, int64_t* parents, int64_t parentsoffset, int64_t length) {
      return awkward_indexedarray32_reduce_next_64(nextcarry, nextparents, index, indexoffset, parents, parentsoffset, length);
    }

    template <>
    Error awkward_indexedarray_reduce_next_64<uint32_t>(int64_t* nextcarry, int64_t* nextparents, const uint32_t* index, int64_t indexoffset, int64_t* parents, int64_t parentsoffset, int64_t length) {
      return awkward_indexedarrayU32_reduce_next_64(nextcarry, nextparents, index, indexoffset, parents, parentsoffset, length);
    }

    template <>
    Error awkward_indexedarray_reduce_next_64<int64_t>(int64_t* nextcarry, int64_t* nextparents, const int64_t* index, int64_t indexoffset, int64_t* parents, int64_t parentsoffset, int64_t length) {
      return awkward_indexedarray64_reduce_next_64(nextcarry, nextparents, index, indexoffset, parents, parentsoffset, length);
    }


  }
}
