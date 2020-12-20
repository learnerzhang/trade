import request from '@/utils/request'
export function getTableData(params) {
  return request({
    url: '/v1/getTableData',
    method: 'post',
    params: {}
  })
}
