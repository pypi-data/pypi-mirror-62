// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <stdexcept>

#include "awkward/Identities.h"
#include "awkward/Index.h"
#include "awkward/array/RecordArray.h"
#include "awkward/array/EmptyArray.h"
#include "awkward/type/RecordType.h"
#include "awkward/type/UnknownType.h"
#include "awkward/fillable/OptionFillable.h"
#include "awkward/fillable/UnionFillable.h"

#include "awkward/fillable/TupleFillable.h"

namespace awkward {
  const std::shared_ptr<Fillable> TupleFillable::fromempty(const FillableOptions& options) {
    std::shared_ptr<Fillable> out = std::make_shared<TupleFillable>(options, std::vector<std::shared_ptr<Fillable>>(), -1, false, -1);
    out.get()->setthat(out);
    return out;
  }

  TupleFillable::TupleFillable(const FillableOptions& options, const std::vector<std::shared_ptr<Fillable>>& contents, int64_t length, bool begun, size_t nextindex)
      : options_(options)
      , contents_(contents)
      , length_(length)
      , begun_(begun)
      , nextindex_(nextindex) { }

  int64_t TupleFillable::numfields() const {
    return (int64_t)contents_.size();
  }

  const std::string TupleFillable::classname() const {
    return "TupleFillable";
  };

  int64_t TupleFillable::length() const {
    return length_;
  }

  void TupleFillable::clear() {
    for (auto x : contents_) {
      x.get()->clear();
    }
    length_ = -1;
    begun_ = false;
    nextindex_ = -1;
  }

  const std::shared_ptr<Content> TupleFillable::snapshot() const {
    if (length_ == -1) {
      return std::make_shared<EmptyArray>(Identities::none(), util::Parameters());
    }
    std::vector<std::shared_ptr<Content>> contents;
    for (size_t i = 0;  i < contents_.size();  i++) {
      contents.push_back(contents_[i].get()->snapshot());
    }
    if (contents.empty()) {
      return std::make_shared<RecordArray>(Identities::none(), util::Parameters(), length_, true);
    }
    else {
      return std::make_shared<RecordArray>(Identities::none(), util::Parameters(), contents);
    }
  }

  bool TupleFillable::active() const {
    return begun_;
  }

  const std::shared_ptr<Fillable> TupleFillable::null() {
    if (!begun_) {
      std::shared_ptr<Fillable> out = OptionFillable::fromvalids(options_, that_);
      out.get()->null();
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'null' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->null());
    }
    else {
      contents_[(size_t)nextindex_].get()->null();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::boolean(bool x) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->boolean(x);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'boolean' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->boolean(x));
    }
    else {
      contents_[(size_t)nextindex_].get()->boolean(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::integer(int64_t x) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->integer(x);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'integer' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->integer(x));
    }
    else {
      contents_[(size_t)nextindex_].get()->integer(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::real(double x) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->real(x);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'real' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->real(x));
    }
    else {
      contents_[(size_t)nextindex_].get()->real(x);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::string(const char* x, int64_t length, const char* encoding) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->string(x, length, encoding);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'string' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->string(x, length, encoding));
    }
    else {
      contents_[(size_t)nextindex_].get()->string(x, length, encoding);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::beginlist() {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->beginlist();
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'beginlist' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->beginlist());
    }
    else {
      contents_[(size_t)nextindex_].get()->beginlist();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::endlist() {
    if (!begun_) {
      throw std::invalid_argument("called 'endlist' without 'beginlist' at the same level before it");
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'endlist' immediately after 'begintuple'; needs 'index' or 'endtuple' and then 'beginlist'");
    }
    else {
      contents_[(size_t)nextindex_].get()->endlist();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::begintuple(int64_t numfields) {
    if (length_ == -1) {
      for (int64_t i = 0;  i < numfields;  i++) {
        contents_.push_back(std::shared_ptr<Fillable>(UnknownFillable::fromempty(options_)));
      }
      length_ = 0;
    }

    if (!begun_  &&  numfields == (int64_t)contents_.size()) {
      begun_ = true;
      nextindex_ = -1;
    }
    else if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->begintuple(numfields);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'begintuple' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->begintuple(numfields));
    }
    else {
      contents_[(size_t)nextindex_].get()->begintuple(numfields);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::index(int64_t index) {
    if (!begun_) {
      throw std::invalid_argument("called 'index' without 'begintuple' at the same level before it");
    }
    else if (nextindex_ == -1  ||  !contents_[(size_t)nextindex_].get()->active()) {
      nextindex_ = index;
    }
    else {
      contents_[(size_t)nextindex_].get()->index(index);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::endtuple() {
    if (!begun_) {
      throw std::invalid_argument("called 'endtuple' without 'begintuple' at the same level before it");
    }
    else if (nextindex_ == -1  ||  !contents_[(size_t)nextindex_].get()->active()) {
      for (size_t i = 0;  i < contents_.size();  i++) {
        if (contents_[i].get()->length() == length_) {
          maybeupdate(i, contents_[i].get()->null());
        }
        if (contents_[i].get()->length() != length_ + 1) {
          throw std::invalid_argument(std::string("tuple index ") + std::to_string(i) + std::string(" filled more than once"));
        }
      }
      length_++;
      begun_ = false;
    }
    else {
      contents_[(size_t)nextindex_].get()->endtuple();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::beginrecord(const char* name, bool check) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->beginrecord(name, check);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'beginrecord' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->beginrecord(name, check));
    }
    else {
      contents_[(size_t)nextindex_].get()->beginrecord(name, check);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::field(const char* key, bool check) {
    if (!begun_) {
      throw std::invalid_argument("called 'field_fast' without 'beginrecord' at the same level before it");
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'field_fast' immediately after 'begintuple'; needs 'index' or 'endtuple' and then 'beginrecord'");
    }
    else {
      contents_[(size_t)nextindex_].get()->field(key, check);
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::endrecord() {
    if (!begun_) {
      throw std::invalid_argument("called 'endrecord' without 'beginrecord' at the same level before it");
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'endrecord' immediately after 'begintuple'; needs 'index' or 'endtuple' and then 'beginrecord'");
    }
    else {
      contents_[(size_t)nextindex_].get()->endrecord();
    }
    return that_;
  }

  const std::shared_ptr<Fillable> TupleFillable::append(const std::shared_ptr<Content>& array, int64_t at) {
    if (!begun_) {
      std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
      out.get()->append(array, at);
      return out;
    }
    else if (nextindex_ == -1) {
      throw std::invalid_argument("called 'append' immediately after 'begintuple'; needs 'index' or 'endtuple'");
    }
    else if (!contents_[(size_t)nextindex_].get()->active()) {
      maybeupdate(nextindex_, contents_[(size_t)nextindex_].get()->append(array, at));
    }
    else {
      contents_[(size_t)nextindex_].get()->append(array, at);
    }
    return that_;
  }

  void TupleFillable::maybeupdate(int64_t i, const std::shared_ptr<Fillable>& tmp) {
    if (tmp.get() != contents_[(size_t)i].get()) {
      contents_[(size_t)i] = tmp;
    }
  }
}
