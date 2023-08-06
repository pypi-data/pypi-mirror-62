// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_REDUCER_H_
#define AWKWARD_REDUCER_H_

#include <memory>

#include "awkward/Index.h"

namespace awkward {
  class EXPORT_SYMBOL Reducer {
  public:
    virtual const std::string name() const = 0;
    virtual const std::string preferred_type() const = 0;
    virtual ssize_t preferred_typesize() const = 0;
    virtual const std::string return_type(const std::string& given_type) const;
    virtual ssize_t return_typesize(const std::string& given_type) const;
    virtual const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
    virtual const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const = 0;
  };

  class EXPORT_SYMBOL ReducerCount: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerCountNonzero: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerSum: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerProd: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerAny: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerAll: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::string return_type(const std::string& given_type) const override;
    ssize_t return_typesize(const std::string& given_type) const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerMin: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

  class EXPORT_SYMBOL ReducerMax: public Reducer {
  public:
    const std::string name() const override;
    const std::string preferred_type() const override;
    ssize_t preferred_typesize() const override;
    const std::shared_ptr<void> apply_bool(const bool* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int8(const int8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint8(const uint8_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int16(const int16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint16(const uint16_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int32(const int32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint32(const uint32_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_int64(const int64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_uint64(const uint64_t* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float32(const float* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
    const std::shared_ptr<void> apply_float64(const double* data, int64_t offset, const Index64& parents, int64_t outlength) const override;
  };

}

#endif // AWKWARD_REDUCER_H_
