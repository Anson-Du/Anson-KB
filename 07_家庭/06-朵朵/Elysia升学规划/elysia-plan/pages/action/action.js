// pages/action/action.js
const { actionTimeline } = require('../../data/schools')

Page({
  data: {
    timeline: [],
    completedCount: 0,
    totalCount: 0,
    progress: 0
  },

  onLoad() {
    // 从本地存储加载完成状态
    const savedState = wx.getStorageSync('actionState') || {}

    const timeline = actionTimeline.map((month, mi) => ({
      ...month,
      tasks: month.tasks.map((task, ti) => ({
        ...task,
        done: savedState[`${mi}-${ti}`] || false
      }))
    }))

    this.setData({ timeline })
    this.calcProgress()
  },

  toggleTask(e) {
    const { mi, ti } = e.currentTarget.dataset
    const key = `${mi}-${ti}`
    const current = this.data.timeline[mi].tasks[ti].done
    const newState = !current

    // 更新UI
    this.setData({
      [`timeline[${mi}].tasks[${ti}].done`]: newState
    })

    // 保存到本地存储
    const savedState = wx.getStorageSync('actionState') || {}
    savedState[key] = newState
    wx.setStorageSync('actionState', savedState)

    this.calcProgress()

    // 完成时震动反馈
    if (newState) {
      wx.vibrateShort({ type: 'light' })
    }
  },

  calcProgress() {
    let total = 0
    let completed = 0
    this.data.timeline.forEach(month => {
      month.tasks.forEach(task => {
        total++
        if (task.done) completed++
      })
    })
    const progress = total > 0 ? Math.round((completed / total) * 100) : 0
    this.setData({
      completedCount: completed,
      totalCount: total,
      progress
    })
  },

  resetProgress() {
    wx.showModal({
      title: '确认重置',
      content: '确定要清除所有完成标记吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('actionState')
          const timeline = actionTimeline.map(month => ({
            ...month,
            tasks: month.tasks.map(task => ({ ...task, done: false }))
          }))
          this.setData({ timeline })
          this.calcProgress()
          wx.showToast({ title: '已重置', icon: 'success' })
        }
      }
    })
  },

  onShareAppMessage() {
    return {
      title: `Elysia升学行动线 · 已完成${this.data.progress}%`,
      path: '/pages/action/action'
    }
  }
})
