// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_ITERATOR_H_
#define AWKWARD_ITERATOR_H_

#include "awkward/cpu-kernels/util.h"
#include "awkward/Content.h"

namespace awkward {
  class EXPORT_SYMBOL Iterator {
  public:
    Iterator(const std::shared_ptr<Content>& content);

    const std::shared_ptr<Content> content() const;
    const int64_t at() const;
    const bool isdone() const;
    const std::shared_ptr<Content> next();
    const std::string tostring_part(const std::string& indent, const std::string& pre, const std::string& post) const;
    const std::string tostring() const;

  private:
    const std::shared_ptr<Content> content_;
    int64_t at_;
  };
}

#endif // AWKWARD_ITERATOR_H_
