import request from "../http/index.js";


export const reqLeaveList=(q)=>request.get(`oa/oa/leave?q=${q}`)
export const reqLeave=(leave_id)=>request.get(`oa/oa/leave/${leave_id}`)
export const reqUpdateLeave=(leave_id,data)=>request.put(`oa/oa/leave/${leave_id}`,{...data})
export const reqDeleteLeave=(ids)=>request.delete('oa/oa/leave',{data:ids})
export const reqCreateLeave=(data)=>request.post('oa/oa/leave',{...data})

export const reqChangeLeaveStatus=(leave_id,status)=>request.get(`oa/oa/leave/status/${leave_id}/${status}`)