// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_FILLABLEARRAY_H_
#define AWKWARD_FILLABLEARRAY_H_

#include "awkward/cpu-kernels/util.h"
#include "awkward/Content.h"
#include "awkward/type/Type.h"
#include "awkward/fillable/FillableOptions.h"
#include "awkward/fillable/Fillable.h"
#include "awkward/fillable/UnknownFillable.h"

namespace awkward {
  class FillableArray {
  public:
    FillableArray(const FillableOptions& options);

    const std::string tostring() const;
    int64_t length() const;
    void clear();
    const std::shared_ptr<Type> type() const;
    const std::shared_ptr<Content> snapshot() const;
    const std::shared_ptr<Content> getitem_at(int64_t at) const;
    const std::shared_ptr<Content> getitem_range(int64_t start, int64_t stop) const;
    const std::shared_ptr<Content> getitem_field(const std::string& key) const;
    const std::shared_ptr<Content> getitem_fields(const std::vector<std::string>& keys) const;
    const std::shared_ptr<Content> getitem(const Slice& where) const;

    void null();
    void boolean(bool x);
    void integer(int64_t x);
    void real(double x);
    void bytestring(const char* x);
    void bytestring(const char* x, int64_t length);
    void bytestring(const std::string& x);
    void string(const char* x);
    void string(const char* x, int64_t length);
    void string(const std::string& x);
    void beginlist();
    void endlist();
    void begintuple(int64_t numfields);
    void index(int64_t index);
    void endtuple();
    void beginrecord();
    void beginrecord_fast(const char* name);
    void beginrecord_check(const char* name);
    void beginrecord_check(const std::string& name);
    void field_fast(const char* key);
    void field_check(const char* key);
    void field_check(const std::string& key);
    void endrecord();
    void append(const std::shared_ptr<Content>& array, int64_t at);
    void append_nowrap(const std::shared_ptr<Content>& array, int64_t at);
    void extend(const std::shared_ptr<Content>& array);

  private:
    void maybeupdate(const std::shared_ptr<Fillable>& tmp);

    static const char* no_encoding;
    static const char* utf8_encoding;

    std::shared_ptr<Fillable> fillable_;
  };
}

extern "C" {
  EXPORT_SYMBOL uint8_t awkward_FillableArray_length(void* fillablearray, int64_t* result);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_clear(void* fillablearray);

  EXPORT_SYMBOL uint8_t awkward_FillableArray_null(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_boolean(void* fillablearray, bool x);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_integer(void* fillablearray, int64_t x);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_real(void* fillablearray, double x);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_bytestring(void* fillablearray, const char* x);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_bytestring_length(void* fillablearray, const char* x, int64_t length);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_string(void* fillablearray, const char* x);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_string_length(void* fillablearray, const char* x, int64_t length);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_beginlist(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_endlist(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_begintuple(void* fillablearray, int64_t numfields);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_index(void* fillablearray, int64_t index);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_endtuple(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_beginrecord(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_beginrecord_fast(void* fillablearray, const char* name);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_beginrecord_check(void* fillablearray, const char* name);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_field_fast(void* fillablearray, const char* key);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_field_check(void* fillablearray, const char* key);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_endrecord(void* fillablearray);
  EXPORT_SYMBOL uint8_t awkward_FillableArray_append_nowrap(void* fillablearray, const void* shared_ptr_ptr, int64_t at);
}

#endif // AWKWARD_FILLABLE_H_
