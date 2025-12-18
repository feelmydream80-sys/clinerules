// @deprecated: This file has been split into smaller modules under /common/api/.
// Please import from the new modules directly.
// This file is kept for backward compatibility of setDataFlowStatus.

import { setDataFlowStatus as newSetDataFlowStatus } from './common/api/client.js';

/**
 * @deprecated Please import from '/common/api/client.js'
 */
export function setDataFlowStatus(statusObject) {
    console.warn("Importing setDataFlowStatus from api.js is deprecated. Please import from /common/api/client.js");
    newSetDataFlowStatus(statusObject);
}
