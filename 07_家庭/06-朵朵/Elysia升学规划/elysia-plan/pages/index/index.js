// pages/index/index.js
const { schoolsData, conclusions } = require('../../data/schools')

Page({
  data: {
    profile: {
      name: 'Elysia',
      age: 16,
      school: '香港蔚来学校 11年级',
      ielts: 5.5,
      ieltsTarget: 7.0,
      strengths: ['数学(AMC奖牌)', '美术/手绘', '二次元文化', '商业直觉(模拟交易ROI 60%)'],
      hkResident: true,
      renewDate: '2027年4月'
    },
    stats: {
      totalSchools: 14,
      totalPrograms: 0,
      regions: 3,
      topMatch: 0
    },
    conclusions: conclusions,
    regionCards: [
      { key: 'uk', emoji: '🇬🇧', name: '英国 G5', count: 5, desc: '剑桥/牛津/帝国/UCL/LSE' },
      { key: 'hk', emoji: '🇭🇰', name: '中国香港', count: 5, desc: '港大/科大/中大/城大/理大' },
      { key: 'japan', emoji: '🇯🇵', name: '日本', count: 4, desc: '东大/京大/筑波/早稻田' }
    ]
  },

  onLoad() {
    // 计算统计数据
    let totalPrograms = 0
    let topMatch = 0
    Object.values(schoolsData).forEach(region => {
      region.schools.forEach(school => {
        totalPrograms += school.programs.length
        school.programs.forEach(p => {
          if (p.match > topMatch) topMatch = p.match
        })
      })
    })
    this.setData({
      'stats.totalPrograms': totalPrograms,
      'stats.topMatch': topMatch
    })
  },

  goToSchools(e) {
    const region = e.currentTarget.dataset.region
    wx.switchTab({
      url: '/pages/schools/schools'
    })
  },

  goToAction() {
    wx.switchTab({
      url: '/pages/action/action'
    })
  },

  goToDetail(e) {
    const { schoolId, programId } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/detail/detail?schoolId=${schoolId}&programId=${programId}`
    })
  },

  copyUrl(e) {
    const url = e.currentTarget.dataset.url
    wx.setClipboardData({
      data: url,
      success() {
        wx.showToast({ title: '链接已复制', icon: 'success' })
      }
    })
  }
})
