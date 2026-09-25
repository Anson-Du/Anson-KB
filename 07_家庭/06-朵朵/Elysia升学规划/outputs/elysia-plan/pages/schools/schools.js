// pages/schools/schools.js
const { schoolsData } = require('../../data/schools')

Page({
  data: {
    currentRegion: 'uk',
    regions: [
      { key: 'uk', name: '🇬🇧 英国G5' },
      { key: 'hk', name: '🇭🇰 香港' },
      { key: 'japan', name: '🇯🇵 日本' }
    ],
    schools: [],
    regionInfo: null,
    filterTag: 'all',
    filters: [
      { key: 'all', name: '全部' },
      { key: 'math', name: '数学' },
      { key: 'datascience', name: '数据科学' },
      { key: 'chemistry', name: '化学' },
      { key: 'mathdesign', name: '数学+设计' }
    ]
  },

  onLoad() {
    this.loadRegion('uk')
  },

  onShow() {
    // 刷新数据
    this.loadRegion(this.data.currentRegion)
  },

  loadRegion(regionKey) {
    const regionData = schoolsData[regionKey]
    if (!regionData) return

    this.setData({
      currentRegion: regionKey,
      schools: regionData.schools,
      regionInfo: {
        region: regionData.region,
        flag: regionData.flag,
        deadline_note: regionData.deadline_note
      }
    })
  },

  switchRegion(e) {
    const region = e.currentTarget.dataset.region
    this.loadRegion(region)
  },

  filterByTag(e) {
    const tag = e.currentTarget.dataset.tag
    this.setData({ filterTag: tag })
  },

  getFilteredPrograms(programs) {
    if (this.data.filterTag === 'all') return programs
    return programs.filter(p => p.tags.includes(this.data.filterTag))
  },

  goToDetail(e) {
    const { schoolId, programId } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/detail/detail?schoolId=${schoolId}&programId=${programId}`
    })
  },

  openUrl(e) {
    const url = e.currentTarget.dataset.url
    wx.setClipboardData({
      data: url,
      success() {
        wx.showToast({ title: '链接已复制', icon: 'success' })
      }
    })
  },

  // 生成星星字符串
  getStars(count) {
    return '★'.repeat(count) + '☆'.repeat(5 - count)
  }
})
