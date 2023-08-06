/*
Copyright (c) by respective owners including Yahoo!, Microsoft, and
individual contributors. All rights reserved.  Released under a BSD
license as described in the file LICENSE.
*/
#pragma once

#include "cb_explore_adf_common.h"
#include "reductions_fwd.h"

namespace VW
{
namespace cb_explore_adf
{
namespace regcb
{
LEARNER::base_learner* setup(VW::config::options_i& options, vw& all);
}  // namespace regcb
}  // namespace cb_explore_adf
}  // namespace VW
