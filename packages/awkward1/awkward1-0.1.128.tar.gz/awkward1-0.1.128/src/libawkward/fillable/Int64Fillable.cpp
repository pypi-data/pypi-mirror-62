// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include "awkward/Identities.h"
#include "awkward/array/NumpyArray.h"
#include "awkward/type/PrimitiveType.h"
#include "awkward/fillable/OptionFillable.h"
#include "awkward/fillable/UnionFillable.h"
#include "awkward/fillable/Float64Fillable.h"

#include "awkward/fillable/Int64Fillable.h"

namespace awkward {
  const std::shared_ptr<Fillable> Int64Fillable::fromempty(const FillableOptions& options) {
    std::shared_ptr<Fillable> out = std::make_shared<Int64Fillable>(options, GrowableBuffer<int64_t>::empty(options));
    out.get()->setthat(out);
    return out;
  }

  Int64Fillable::Int64Fillable(const FillableOptions& options, const GrowableBuffer<int64_t>& buffer)
      : options_(options)
      , buffer_(buffer) { }

  const GrowableBuffer<int64_t> Int64Fillable::buffer() const {
    return buffer_;
  }

  const std::string Int64Fillable::classname() const {
    return "Int64Fillable";
  };

  int64_t Int64Fillable::length() const {
    return buffer_.length();
  }

  void Int64Fillable::clear() {
    buffer_.clear();
  }

  const std::shared_ptr<Content> Int64Fillable::snapshot() const {
    std::vector<ssize_t> shape = { (ssize_t)buffer_.length() };
    std::vector<ssize_t> strides = { (ssize_t)sizeof(int64_t) };
#if defined _MSC_VER || defined __i386__
    return std::make_shared<NumpyArray>(Identities::none(), util::Parameters(), buffer_.ptr(), shape, strides, 0, sizeof(int64_t), "q");
#else
    return std::make_shared<NumpyArray>(Identities::none(), util::Parameters(), buffer_.ptr(), shape, strides, 0, sizeof(int64_t), "l");
#endif
  }

  bool Int64Fillable::active() const {
    return false;
  }

  const std::shared_ptr<Fillable> Int64Fillable::null() {
    std::shared_ptr<Fillable> out = OptionFillable::fromvalids(options_, that_);
    out.get()->null();
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::boolean(bool x) {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->boolean(x);
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::integer(int64_t x) {
    buffer_.append(x);
    return that_;
  }

  const std::shared_ptr<Fillable> Int64Fillable::real(double x) {
    std::shared_ptr<Fillable> out = Float64Fillable::fromint64(options_, buffer_);
    out.get()->real(x);
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::string(const char* x, int64_t length, const char* encoding) {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->string(x, length, encoding);
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::beginlist() {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->beginlist();
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::endlist() {
    throw std::invalid_argument("called 'endlist' without 'beginlist' at the same level before it");
  }

  const std::shared_ptr<Fillable> Int64Fillable::begintuple(int64_t numfields) {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->begintuple(numfields);
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::index(int64_t index) {
    throw std::invalid_argument("called 'index' without 'begintuple' at the same level before it");
  }

  const std::shared_ptr<Fillable> Int64Fillable::endtuple() {
    throw std::invalid_argument("called 'endtuple' without 'begintuple' at the same level before it");
  }

  const std::shared_ptr<Fillable> Int64Fillable::beginrecord(const char* name, bool check) {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->beginrecord(name, check);
    return out;
  }

  const std::shared_ptr<Fillable> Int64Fillable::field(const char* key, bool check) {
    throw std::invalid_argument("called 'field' without 'beginrecord' at the same level before it");
  }

  const std::shared_ptr<Fillable> Int64Fillable::endrecord() {
    throw std::invalid_argument("called 'endrecord' without 'beginrecord' at the same level before it");
  }

  const std::shared_ptr<Fillable> Int64Fillable::append(const std::shared_ptr<Content>& array, int64_t at) {
    std::shared_ptr<Fillable> out = UnionFillable::fromsingle(options_, that_);
    out.get()->append(array, at);
    return out;
  }
}
