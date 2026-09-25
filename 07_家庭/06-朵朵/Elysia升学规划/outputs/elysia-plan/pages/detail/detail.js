// pages/detail/detail.js
const { schoolsData } = require('../../data/schools')

Page({
  data: {
    school: null,
    program: null,
    schoolId: '',
    programId: ''
  },

  onLoad(options) {
    const { schoolId, programId } = options
    this.setData({ schoolId, programId })

    // 查找院校和专业
    let school = null
    let program = null

    for (const region of Object.values(schoolsData)) {
      for (const s of region.schools) {
        if (s.id === schoolId) {
          school = s
          for (const p of s.programs) {
            if (p.id === programId) {
              program = p
              break
            }
          }
          break
        }
      }
      if (school) break
    }

    if (school && program) {
      // 生成星星
      const matchStars = '★'.repeat(program.match) + '☆'.repeat(5 - program.match)
      const schoolStars = '★'.repeat(school.matchScore) + '☆'.repeat(5 - school.matchScore)

      this.setData({
        school,
        program,
        matchStars,
        schoolStars,
        tagLabels: program.tags.map(t => {
          const map = { math: '数学', datascience: '数据科学', chemistry: '化学', mathdesign: '数学+设计' }
          return map[t] || t
        })
      })
    }
  },

  openUrl() {
    if (this.data.program && this.data.program.url) {
      wx.setClipboardData({
        data: this.data.program.url,
        success() {
          wx.showModal({
            title: '链接已复制',
            content: this.data.program.url,
            confirmText: '去浏览器打开',
            showCancel: true,
            cancelText: '关闭'
          })
        }
      })
    }
  },

  shareProgram() {
    wx.showShareMenu({
      withShareTicket: true
    })
  },

  onShareAppMessage() {
    const { school, program } = this.data
    return {
      title: `${school.name} - ${program.nameCn} | Elysia升学攻略`,
      path: `/pages/detail/detail?schoolId=${this.data.schoolId}&programId=${this.data.programId}`
    }
  }
})
