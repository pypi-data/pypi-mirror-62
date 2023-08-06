// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <stdexcept>

#include "awkward/Identities.h"
#include "awkward/Index.h"
#include "awkward/type/UnionType.h"
#include "awkward/builder/OptionBuilder.h"
#include "awkward/builder/BoolBuilder.h"
#include "awkward/builder/Int64Builder.h"
#include "awkward/builder/Float64Builder.h"
#include "awkward/builder/StringBuilder.h"
#include "awkward/builder/ListBuilder.h"
#include "awkward/builder/TupleBuilder.h"
#include "awkward/builder/RecordBuilder.h"
#include "awkward/builder/IndexedBuilder.h"
#include "awkward/array/UnionArray.h"

#include "awkward/builder/UnionBuilder.h"

namespace awkward {
  const std::shared_ptr<Builder> UnionBuilder::fromsingle(const ArrayBuilderOptions& options, const std::shared_ptr<Builder>& firstcontent) {
    GrowableBuffer<int8_t> types = GrowableBuffer<int8_t>::full(options, 0, firstcontent->length());
    GrowableBuffer<int64_t> offsets = GrowableBuffer<int64_t>::arange(options, firstcontent->length());
    std::vector<std::shared_ptr<Builder>> contents({ firstcontent });
    std::shared_ptr<Builder> out = std::make_shared<UnionBuilder>(options, types, offsets, contents);
    out.get()->setthat(out);
    return out;
  }

  UnionBuilder::UnionBuilder(const ArrayBuilderOptions& options, const GrowableBuffer<int8_t>& types, const GrowableBuffer<int64_t>& offsets, std::vector<std::shared_ptr<Builder>>& contents)
      : options_(options)
      , types_(types)
      , offsets_(offsets)
      , contents_(contents)
      , current_(-1) { }

  const std::string UnionBuilder::classname() const {
    return "UnionBuilder";
  };

  int64_t UnionBuilder::length() const {
    return types_.length();
  }

  void UnionBuilder::clear() {
    types_.clear();
    offsets_.clear();
    for (auto x : contents_) {
      x.get()->clear();
    }
  }

  const std::shared_ptr<Content> UnionBuilder::snapshot() const {
    Index8 tags(types_.ptr(), 0, types_.length());
    Index64 index(offsets_.ptr(), 0, offsets_.length());
    std::vector<std::shared_ptr<Content>> contents;
    for (auto content : contents_) {
      contents.push_back(content.get()->snapshot());
    }
    return std::make_shared<UnionArray8_64>(Identities::none(), util::Parameters(), tags, index, contents);
  }

  bool UnionBuilder::active() const {
    return current_ != -1;
  }

  const std::shared_ptr<Builder> UnionBuilder::null() {
    if (current_ == -1) {
      std::shared_ptr<Builder> out = OptionBuilder::fromvalids(options_, that_);
      out.get()->null();
      return out;
    }
    else {
      contents_[(size_t)current_].get()->null();
      return that_;
    }
  }

  const std::shared_ptr<Builder> UnionBuilder::boolean(bool x) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (dynamic_cast<BoolBuilder*>(content.get()) != nullptr) {
          tofill = content;
          break;
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = BoolBuilder::fromempty(options_);
        contents_.push_back(tofill);
      }
      int64_t length = tofill.get()->length();
      tofill.get()->boolean(x);
      types_.append(i);
      offsets_.append(length);
    }
    else {
      contents_[(size_t)current_].get()->boolean(x);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::integer(int64_t x) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (dynamic_cast<Int64Builder*>(content.get()) != nullptr) {
          tofill = content;
          break;
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = Int64Builder::fromempty(options_);
        contents_.push_back(tofill);
      }
      int64_t length = tofill.get()->length();
      tofill.get()->integer(x);
      types_.append(i);
      offsets_.append(length);
    }
    else {
      contents_[(size_t)current_].get()->integer(x);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::real(double x) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (dynamic_cast<Float64Builder*>(content.get()) != nullptr) {
          tofill = content;
          break;
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        i = 0;
        for (auto content : contents_) {
          if (dynamic_cast<Int64Builder*>(content.get()) != nullptr) {
            tofill = content;
            break;
          }
          i++;
        }
        if (tofill.get() != nullptr) {
          tofill = Float64Builder::fromint64(options_, dynamic_cast<Int64Builder*>(tofill.get())->buffer());
          contents_[(size_t)i] = tofill;
        }
        else {
          tofill = Float64Builder::fromempty(options_);
          contents_.push_back(tofill);
        }
      }
      int64_t length = tofill.get()->length();
      tofill.get()->real(x);
      types_.append(i);
      offsets_.append(length);
    }
    else {
      contents_[(size_t)current_].get()->real(x);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::string(const char* x, int64_t length, const char* encoding) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (StringBuilder* raw = dynamic_cast<StringBuilder*>(content.get())) {
          if (raw->encoding() == encoding) {
            tofill = content;
            break;
          }
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = StringBuilder::fromempty(options_, encoding);
        contents_.push_back(tofill);
      }
      int64_t len = tofill.get()->length();
      tofill.get()->string(x, length, encoding);
      types_.append(i);
      offsets_.append(len);
    }
    else {
      contents_[(size_t)current_].get()->string(x, length, encoding);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::beginlist() {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (dynamic_cast<ListBuilder*>(content.get()) != nullptr) {
          tofill = content;
          break;
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = ListBuilder::fromempty(options_);
        contents_.push_back(tofill);
      }
      tofill->beginlist();
      current_ = i;
    }
    else {
      contents_[(size_t)current_].get()->beginlist();
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::endlist() {
    if (current_ == -1) {
      throw std::invalid_argument("called 'endlist' without 'beginlist' at the same level before it");
    }
    else {
      int64_t length = contents_[(size_t)current_].get()->length();
      contents_[(size_t)current_].get()->endlist();
      if (length != contents_[(size_t)current_].get()->length()) {
        types_.append(current_);
        offsets_.append(length);
        current_ = -1;
      }
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::begintuple(int64_t numfields) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (TupleBuilder* raw = dynamic_cast<TupleBuilder*>(content.get())) {
          if (raw->length() == -1  ||  raw->numfields() == numfields) {
            tofill = content;
            break;
          }
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = TupleBuilder::fromempty(options_);
        contents_.push_back(tofill);
      }
      tofill->begintuple(numfields);
      current_ = i;
    }
    else {
      contents_[(size_t)current_].get()->begintuple(numfields);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::index(int64_t index) {
    if (current_ == -1) {
      throw std::invalid_argument("called 'index' without 'begintuple' at the same level before it");
    }
    else {
      contents_[(size_t)current_].get()->index(index);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::endtuple() {
    if (current_ == -1) {
      throw std::invalid_argument("called 'endtuple' without 'begintuple' at the same level before it");
    }
    else {
      int64_t length = contents_[(size_t)current_].get()->length();
      contents_[(size_t)current_].get()->endtuple();
      if (length != contents_[(size_t)current_].get()->length()) {
        types_.append(current_);
        offsets_.append(length);
        current_ = -1;
      }
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::beginrecord(const char* name, bool check) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (RecordBuilder* raw = dynamic_cast<RecordBuilder*>(content.get())) {
          if (raw->length() == -1  ||  ((check  &&  raw->name() == name)  ||  (!check  &&  raw->nameptr() == name))) {
            tofill = content;
            break;
          }
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = RecordBuilder::fromempty(options_);
        contents_.push_back(tofill);
      }
      tofill->beginrecord(name, check);
      current_ = i;
    }
    else {
      contents_[(size_t)current_].get()->beginrecord(name, check);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::field(const char* key, bool check) {
    if (current_ == -1) {
      throw std::invalid_argument("called 'field' without 'beginrecord' at the same level before it");
    }
    else {
      contents_[(size_t)current_].get()->field(key, check);
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::endrecord() {
    if (current_ == -1) {
      throw std::invalid_argument("called 'endrecord' without 'beginrecord' at the same level before it");
    }
    else {
      int64_t length = contents_[(size_t)current_].get()->length();
      contents_[(size_t)current_].get()->endrecord();
      if (length != contents_[(size_t)current_].get()->length()) {
        types_.append(current_);
        offsets_.append(length);
        current_ = -1;
      }
    }
    return that_;
  }

  const std::shared_ptr<Builder> UnionBuilder::append(const std::shared_ptr<Content>& array, int64_t at) {
    if (current_ == -1) {
      std::shared_ptr<Builder> tofill(nullptr);
      int8_t i = 0;
      for (auto content : contents_) {
        if (IndexedGenericBuilder* raw = dynamic_cast<IndexedGenericBuilder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        else if (IndexedI32Builder* raw = dynamic_cast<IndexedI32Builder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        else if (IndexedIU32Builder* raw = dynamic_cast<IndexedIU32Builder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        else if (IndexedI64Builder* raw = dynamic_cast<IndexedI64Builder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        else if (IndexedIO32Builder* raw = dynamic_cast<IndexedIO32Builder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        else if (IndexedIO64Builder* raw = dynamic_cast<IndexedIO64Builder*>(content.get())) {
          if (raw->arrayptr() == array.get()) {
            tofill = content;
            break;
          }
        }
        i++;
      }
      if (tofill.get() == nullptr) {
        tofill = IndexedGenericBuilder::fromnulls(options_, 0, array);
        contents_.push_back(tofill);
      }
      int64_t length = tofill.get()->length();
      tofill.get()->append(array, at);
      types_.append(i);
      offsets_.append(length);
    }
    else {
      contents_[(size_t)current_].get()->append(array, at);
    }
    return that_;
  }
}
