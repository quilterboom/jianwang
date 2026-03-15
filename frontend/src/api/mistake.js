import request from '@/utils/request'

// 获取记录列表
export function getMistakeRecords(params) {
  return request({
    url: '/mistake-records/',
    method: 'get',
    params
  })
}

// 创建记录
export function createMistakeRecord(data) {
  return request({
    url: '/mistake-records/',
    method: 'post',
    data
  })
}

// 获取记录详情
export function getMistakeRecord(id) {
  return request({
    url: `/mistake-records/${id}/`,
    method: 'get'
  })
}

// 更新记录
export function updateMistakeRecord(id, data) {
  return request({
    url: `/mistake-records/${id}/`,
    method: 'put',
    data
  })
}

// 删除记录
export function deleteMistakeRecord(id) {
  return request({
    url: `/mistake-records/${id}/`,
    method: 'delete'
  })
}
