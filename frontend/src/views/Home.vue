<template>
  <div class="home-container">
    <!-- 头部 -->
    <el-header class="header">
      <div class="header-left">
        <h1 class="logo">鉴往</h1>
        <span class="subtitle">投资犯错记录系统</span>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ userProfile?.username || '用户' }}
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <!-- 主内容 -->
    <el-main class="main">
      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :xs="24" :sm="12" :md="12">
          <el-card class="stats-card mistake-card" shadow="hover">
            <div class="stats-content">
              <div class="stats-info">
                <p class="stats-label">累计犯错次数</p>
                <p class="stats-value mistake-count">{{ userProfile?.mistake_count || 0 }}</p>
              </div>
              <div class="stats-icon">
                <el-icon size="64" color="#f56c6c"><Warning /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12">
          <el-card class="stats-card success-card" shadow="hover">
            <div class="stats-content">
              <div class="stats-info">
                <p class="stats-label">无犯错记录天数</p>
                <p class="stats-value success-count">{{ userProfile?.no_mistake_days || 0 }}</p>
              </div>
              <div class="stats-icon">
                <el-icon size="64" color="#67c23a"><Calendar /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 记录表单 -->
      <el-card class="form-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>记录新的错误</span>
          </div>
        </template>
        
        <el-form
          ref="mistakeFormRef"
          :model="mistakeForm"
          :rules="mistakeRules"
          label-width="100px"
        >
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="投资类型" prop="investment_type">
                <el-select
                  v-model="mistakeForm.investment_type"
                  placeholder="请选择投资类型"
                  style="width: 100%"
                  size="large"
                >
                  <el-option
                    v-for="item in investmentTypes"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="当前时间">
                <el-input :value="currentTime" disabled size="large" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="犯错原因" prop="reason">
            <el-input
              v-model="mistakeForm.reason"
              type="textarea"
              :rows="4"
              placeholder="请详细描述犯错的原因、经过和反思..."
              size="large"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="submitting"
              @click="handleSubmit"
            >
              <el-icon><Check /></el-icon>
              保存记录
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 历史记录 -->
      <el-card class="records-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>历史犯错记录</span>
            <el-tag type="info">{{ records.length }} 条记录</el-tag>
          </div>
        </template>
        
        <el-timeline v-if="records.length > 0" class="records-timeline">
          <el-timeline-item
            v-for="record in records"
            :key="record.id"
            :timestamp="record.created_at_formatted"
            placement="top"
          >
            <template #icon>
              <el-icon color="#f56c6c"><Warning /></el-icon>
            </template>
            <el-card class="record-card" shadow="hover">
              <div class="record-header">
                <el-tag :type="getTagType(record.investment_type)">
                  {{ record.investment_type_display }}
                </el-tag>
              </div>
              <p class="record-reason">{{ record.reason }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
        
        <el-empty v-else description="暂无犯错记录，继续保持！" />
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElForm, ElMessageBox } from 'element-plus'
import { User, Warning, Calendar, Check } from '@element-plus/icons-vue'
import { getProfile, getInvestmentTypes, logout } from '@/api/auth'
import { getMistakeRecords, createMistakeRecord } from '@/api/mistake'

const router = useRouter()
const mistakeFormRef = ref()
const userProfile = ref(null)
const investmentTypes = ref([])
const records = ref([])
const submitting = ref(false)
const loading = ref(false)

const currentTime = computed(() => {
  return new Date().toLocaleString('zh-CN')
})

const mistakeForm = ref({
  investment_type: '',
  reason: ''
})

const mistakeRules = {
  investment_type: [
    { required: true, message: '请选择投资类型', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入犯错原因', trigger: 'blur' },
    { min: 5, message: '原因描述不能少于5个字符', trigger: 'blur' }
  ]
}

const getTagType = (type) => {
  const typeMap = {
    crypto: 'danger',
    stock: 'warning',
    fund: 'success',
    bond: 'info',
    futures: 'danger',
    options: 'warning',
    real_estate: 'primary',
    other: 'info'
  }
  return typeMap[type] || 'info'
}

const loadProfile = async () => {
  try {
    userProfile.value = await getProfile()
  } catch (error) {
    console.error('加载用户信息失败:', error)
  }
}

const loadInvestmentTypes = async () => {
  try {
    investmentTypes.value = await getInvestmentTypes()
  } catch (error) {
    console.error('加载投资类型失败:', error)
  }
}

const loadRecords = async () => {
  try {
    loading.value = true
    records.value = await getMistakeRecords()
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!mistakeFormRef.value) return
  
  await mistakeFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await ElMessageBox.confirm(
          '保存后无犯错记录天数将归零，是否确认保存？',
          '确认提交',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const result = await createMistakeRecord(mistakeForm.value)
        userProfile.value = result.profile
        ElMessage.success('记录保存成功！无犯错天数已归零')
        
        // 重置表单
        mistakeForm.value = {
          investment_type: '',
          reason: ''
        }
        mistakeFormRef.value.resetFields()
        
        // 重新加载记录
        await loadRecords()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('保存失败:', error)
        }
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm(
        '确定要退出登录吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      await logout()
      ElMessage.success('退出登录成功')
      router.push('/login')
    } catch (error) {
      if (error !== 'cancel') {
        console.error('退出失败:', error)
      }
    }
  }
}

onMounted(async () => {
  await loadProfile()
  await loadInvestmentTypes()
  await loadRecords()
  
  // 每分钟更新一次当前时间
  setInterval(() => {
    // 触发computed更新
  }, 60000)
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin: 0;
}

.subtitle {
  color: #909399;
  font-size: 14px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
  cursor: pointer;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.mistake-card {
  border-left: 4px solid #f56c6c;
}

.success-card {
  border-left: 4px solid #67c23a;
}

.stats-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.stats-value {
  font-size: 36px;
  font-weight: bold;
  margin: 0;
}

.mistake-count {
  color: #f56c6c;
}

.success-count {
  color: #67c23a;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
  font-size: 16px;
}

.records-card {
  margin-bottom: 20px;
}

.records-timeline {
  padding: 20px 0;
}

.record-card {
  margin-bottom: 10px;
}

.record-header {
  margin-bottom: 10px;
}

.record-reason {
  color: #606266;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}
</style>
