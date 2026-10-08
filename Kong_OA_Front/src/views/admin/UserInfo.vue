
<template>
  <div class="user-info-container">
    <el-card class="user-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>

          <el-button
            type="primary"
            :icon="Edit"
            @click="handleEdit"
          >
            编辑资料
          </el-button>
        </div>
      </template>

      <div class="user-content">

        <!-- 左侧头像区域 -->
        <div class="user-avatar">
         <el-avatar :size="120" :src="`http://127.0.0.1:8080/media/${userInfo.avatar}`">
            {{ userInfo.nick_name || userInfo.username }}
          </el-avatar>

          <div class="username">
            {{ userInfo.nick_name || userInfo.username }}
          </div>

          <div class="account">
            @{{ userInfo.username }}
          </div>

          <el-tag
            v-if="userInfo.enabled"
            type="success"
            class="status-tag"
          >
            已启用
          </el-tag>

          <el-tag
            v-else
            type="danger"
            class="status-tag"
          >
            已禁用
          </el-tag>
        </div>

        <!-- 右侧用户信息 -->
        <div class="user-detail">

          <el-descriptions
            title="基本信息"
            :column="2"
            border
          >

            <el-descriptions-item label="用户名">
              {{ userInfo.username || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="昵称">
              {{ userInfo.nick_name || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="性别">
              {{ getGenderText(userInfo.gender) }}
            </el-descriptions-item>

            <el-descriptions-item label="邮箱">
              {{ userInfo.email || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="手机号">
              {{ userInfo.phone || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="部门">
              {{ userInfo.dept?.name || '-' }}
            </el-descriptions-item>

            <el-descriptions-item label="岗位">
              <template v-if="userInfo.job?.length">
                <el-tag
                  v-for="item in userInfo.job"
                  :key="item.id"
                  class="tag-item"
                >
                  {{ item.name }}
                </el-tag>
              </template>

              <span v-else>-</span>
            </el-descriptions-item>

            <el-descriptions-item label="角色">
              <template v-if="userInfo.roles?.length">
                <el-tag
                  v-for="item in userInfo.roles"
                  :key="item.id"
                  type="warning"
                  class="tag-item"
                >
                  {{ item.name }}
                </el-tag>
              </template>

              <span v-else>-</span>
            </el-descriptions-item>

            <el-descriptions-item label="超级管理员">
              <el-tag
                v-if="userInfo.is_superuser"
                type="danger"
              >
                是
              </el-tag>

              <el-tag v-else type="info">
                否
              </el-tag>
            </el-descriptions-item>

            <el-descriptions-item label="账号状态">
              <el-tag
                v-if="userInfo.is_active"
                type="success"
              >
                正常
              </el-tag>

              <el-tag v-else type="danger">
                禁用
              </el-tag>
            </el-descriptions-item>

          </el-descriptions>

          <!-- 修改密码 -->
          <div class="password-area">
            <el-button
              type="warning"
              :icon="Lock"
              @click="passwordDialogVisible = true"
            >
              修改密码
            </el-button>
          </div>

        </div>
      </div>
    </el-card>

    <!-- 编辑个人资料 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑个人资料"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="editForm"
        :rules="rules"
        label-width="80px"
      >

        <el-form-item label="昵称" prop="nick_name">
          <el-input
            v-model="editForm.nick_name"
            placeholder="请输入昵称"
          />
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editForm.gender">
            <el-radio value="男">男</el-radio>
            <el-radio value="女">女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="editForm.phone"
            placeholder="请输入手机号"
          />
        </el-form-item>

      </el-form>

      <template #footer>
        <el-button @click="editDialogVisible = false">
          取消
        </el-button>

        <el-button
          type="primary"
          :loading="editLoading"
          @click="handleSave"
        >
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 修改密码 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="修改密码"
      width="500px"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >

        <el-form-item label="原密码" prop="old_password">
          <el-input
            v-model="passwordForm.old_password"
            type="password"
            show-password
            placeholder="请输入原密码"
          />
        </el-form-item>

        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="password"
            show-password
            placeholder="请输入新密码"
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirm_password">
          <el-input
            v-model="passwordForm.confirm_password"
            type="password"
            show-password
            placeholder="请再次输入新密码"
          />
        </el-form-item>

      </el-form>

      <template #footer>
        <el-button @click="passwordDialogVisible = false">
          取消
        </el-button>

        <el-button
          type="primary"
          :loading="passwordLoading"
          @click="handleChangePassword"
        >
          确定修改
        </el-button>
      </template>
    </el-dialog>

  </div>
</template>


<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { reqUserInfo, reqUpdateUserInfo,reqChangePassword } from '../../api/user'
import { Edit, Lock } from '@element-plus/icons-vue'


const userInfo = ref({
  id: null,
  username: '',
  email: '',
  nick_name: '',
  gender: '',
  phone: '',
  avatar: '',
  enabled: true,
  is_active: true,
  is_superuser: false,
  dept: null,
  roles: [],
  job: []
})

// 获取当前登录用户信息
const getUserInfo = async () => {
  try {
    const res = await reqUserInfo()

    console.log('用户信息：', res)

    // APIResponse 中真正的用户数据在 result 里面
    userInfo.value = res.result
  } catch (error) {
    console.error('获取用户信息失败：', error)
    ElMessage.error('获取用户信息失败')
  }
}

// 编辑表单
const editDialogVisible = ref(false)

const editForm = reactive({
  nick_name: '',
  email: '',
  gender: '',
  phone: ''
})

const handleEdit = () => {
  editForm.nick_name = userInfo.value.nick_name
  editForm.email = userInfo.value.email
  editForm.gender = userInfo.value.gender
  editForm.phone = userInfo.value.phone

  editDialogVisible.value = true
}

const editLoading = ref(false)

const handleSave = async () => {
  try {
    // 开启保存按钮 loading
    editLoading.value = true

    // 调用后端接口
    const res = await reqUpdateUserInfo({
      nick_name: editForm.nick_name,
      email: editForm.email,
      gender: editForm.gender,
      phone: editForm.phone
    })

    console.log('修改用户信息返回：', res)

    // 后端返回修改后的完整用户信息
    if (res.result) {
      userInfo.value = res.result
    }

    ElMessage.success(res.msg || '保存成功')

    // 关闭弹窗
    editDialogVisible.value = false

  } catch (error) {
    console.error('修改用户信息失败：', error)
    ElMessage.error('修改用户信息失败')
  } finally {
    editLoading.value = false
  }
}





// 修改密码
// 修改密码
const passwordDialogVisible = ref(false)
const passwordLoading = ref(false)
const passwordFormRef = ref(null)

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 修改密码表单校验
const passwordRules = {
  old_password: [
    {
      required: true,
      message: '请输入原密码',
      trigger: 'blur'
    }
  ],

  new_password: [
    {
      required: true,
      message: '请输入新密码',
      trigger: 'blur'
    },
    {
      min: 6,
      message: '新密码长度不能少于6位',
      trigger: 'blur'
    }
  ],

  confirm_password: [
    {
      required: true,
      message: '请再次输入新密码',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的新密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 打开修改密码弹窗
const handlePassword = () => {
  passwordForm.old_password = ''
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''

  passwordDialogVisible.value = true
}

// 修改密码
const handleChangePassword = async () => {
  try {
    // 先进行表单校验
    await passwordFormRef.value.validate()

    passwordLoading.value = true

    // 调用后端修改密码接口
    const res = await reqChangePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      confirm_password: passwordForm.confirm_password
    })

    console.log('修改密码返回：', res)

    ElMessage.success(res.msg || '密码修改成功')

    // 修改成功后关闭弹窗
    passwordDialogVisible.value = false

    // 清空密码
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''

  } catch (error) {
    // Element Plus 表单校验失败，不需要提示“修改失败”
    if (error === false) {
      return
    }

    console.error('修改密码失败：', error)

    ElMessage.error(
      error?.response?.data?.msg || '密码修改失败'
    )
  } finally {
    passwordLoading.value = false
  }
}

// 性别显示
const getGenderText = (gender) => {
  if (gender === '男') {
    return '男'
  }

  if (gender === '女') {
    return '女'
  }

  return '-'
}

// 页面加载时获取用户信息
onMounted(() => {
  getUserInfo()
})
</script>