import request from '@/utils/request'

export function getIndustryData() {
  return request({
    url: '/share/industry',
    method: 'post',
    params: {}
  })
}
