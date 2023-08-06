// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <stdexcept>

#include "awkward/Identities.h"
#include "awkward/Index.h"
#include "awkward/array/IndexedArray.h"
#include "awkward/type/OptionType.h"

#include "awkward/fillable/OptionFillable.h"

namespace awkward {
  const std::shared_ptr<Fillable> OptionFillable::fromnulls(const FillableOptions& options, int64_t nullcount, const std::shared_ptr<Fillable>& content) {
    GrowableBuffer<int64_t> offsets = GrowableBuffer<int64_t>::full(options, -1, nullcount);
    std::shared_ptr<Fillable> out = std::make_shared<OptionFillable>(options, offsets, content);
    out.get()->setthat(out);
    return out;
  }

  const std::shared_ptr<Fillable> OptionFillable::fromvalids(const FillableOptions& options, const std::shared_ptr<Fillable>& content) {
    GrowableBuffer<int64_t> offsets = GrowableBuffer<int64_t>::arange(options, content->length());
    std::shared_ptr<Fillable> out = std::make_shared<OptionFillable>(options, offsets, content);
    out.get()->setthat(out);
    return out;
  }

  OptionFillable::OptionFillable(const FillableOptions& options, const GrowableBuffer<int64_t>& offsets, const std::shared_ptr<Fillable>& content)
      : options_(options)
      , offsets_(offsets)
      , content_(content) { }

  const std::string OptionFillable::classname() const {
    return "OptionFillable";
  };

  int64_t OptionFillable::length() const {
    return offsets_.length();
  }

  void OptionFillable::clear() {
    offsets_.clear();
    content_.get()->clear();
  }

  const std::shared_ptr<Content> OptionFillable::snapshot() const {
    Index64 index(offsets_.ptr(), 0, offsets_.length());
    return std::make_shared<IndexedOptionArray64>(Identities::none(), util::Parameters(), index, content_.get()->snapshot());
  }

  bool OptionFillable::active() const {
    return content_.get()->active();
  }

  const std::shared_ptr<Fillable> OptionFillable::null() {
    if (!content_.get()->active()) {
      offsets_.append(-1);
    }
    else {
      content_.get()->null();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::boolean(bool x) {
    if (!content_.get()->active()) {
      int64_t length = content_.get()->length();
      maybeupdate(content_.get()->boolean(x));
      offsets_.append(length);
    }
    else {
      content_.get()->boolean(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::integer(int64_t x) {
    if (!content_.get()->active()) {
      int64_t length = content_.get()->length();
      maybeupdate(content_.get()->integer(x));
      offsets_.append(length);
    }
    else {
      content_.get()->integer(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::real(double x) {
    if (!content_.get()->active()) {
      int64_t length = content_.get()->length();
      maybeupdate(content_.get()->real(x));
      offsets_.append(length);
    }
    else {
      content_.get()->real(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::string(const char* x, int64_t length, const char* encoding) {
    if (!content_.get()->active()) {
      int64_t len = content_.get()->length();
      maybeupdate(content_.get()->string(x, length, encoding));
      offsets_.append(len);
    }
    else {
      content_.get()->string(x, length, encoding);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::beginlist() {
    if (!content_.get()->active()) {
      maybeupdate(content_.get()->beginlist());
    }
    else {
      content_.get()->beginlist();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::endlist() {
    if (!content_.get()->active()) {
      throw std::invalid_argument("called 'endlist' without 'beginlist' at the same level before it");
    }
    else {
      int64_t length = content_.get()->length();
      content_.get()->endlist();
      if (length != content_.get()->length()) {
        offsets_.append(length);
      }
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::begintuple(int64_t numfields) {
    if (!content_.get()->active()) {
      maybeupdate(content_.get()->begintuple(numfields));
    }
    else {
      content_.get()->begintuple(numfields);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::index(int64_t index) {
    if (!content_.get()->active()) {
      throw std::invalid_argument("called 'index' without 'begintuple' at the same level before it");
    }
    else {
      content_.get()->index(index);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::endtuple() {
    if (!content_.get()->active()) {
      throw std::invalid_argument("called 'endtuple' without 'begintuple' at the same level before it");
    }
    else {
      int64_t length = content_.get()->length();
      content_.get()->endtuple();
      if (length != content_.get()->length()) {
        offsets_.append(length);
      }
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::beginrecord(const char* name, bool check) {
    if (!content_.get()->active()) {
      maybeupdate(content_.get()->beginrecord(name, check));
    }
    else {
      content_.get()->beginrecord(name, check);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::field(const char* key, bool check) {
    if (!content_.get()->active()) {
      throw std::invalid_argument("called 'field' without 'beginrecord' at the same level before it");
    }
    else {
      content_.get()->field(key, check);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::endrecord() {
    if (!content_.get()->active()) {
      throw std::invalid_argument("called 'endrecord' without 'beginrecord' at the same level before it");
    }
    else {
      int64_t length = content_.get()->length();
      content_.get()->endrecord();
      if (length != content_.get()->length()) {
        offsets_.append(length);
      }
    }
    return that_;
  }

  const std::shared_ptr<Fillable> OptionFillable::append(const std::shared_ptr<Content>& array, int64_t at) {
    if (!content_.get()->active()) {
      int64_t length = content_.get()->length();
      maybeupdate(content_.get()->append(array, at));
      offsets_.append(length);
    }
    else {
      content_.get()->append(array, at);
    }
    return that_;
  }

  void OptionFillable::maybeupdate(const std::shared_ptr<Fillable>& tmp) {
    if (tmp.get() != content_.get()) {
      content_ = tmp;
    }
  }
}
