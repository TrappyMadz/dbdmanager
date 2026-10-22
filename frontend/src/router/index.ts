import type { RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomeView.vue'
import PatchNotes from '@/views/PatchNotesView.vue'
import AdminPatchNotes from '@/views/AdminPatchNotesView.vue'
import AdminPatchNotesEdit from '@/views/AdminPatchNotesEditView.vue'
import AdminPatchNotesNew from '@/views/AdminPatchNotesNewView.vue'
import NotFound from '@/views/NotFoundView.vue'

const  routes: RouteRecordRaw[] = [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/patchnotes',
      name: 'PatchNotes',
      component: PatchNotes
    },
    {
      path: '/admin/patchnotes',
      name: 'AdminPatchNotes',
      component: AdminPatchNotes
    },
    {
      path: '/admin/patchnotes/edit/:id',
      name: 'AdminPatchNotesEdit',
      component: AdminPatchNotesEdit
    },
    {
      path: '/admin/patchnotes/new',
      name: 'AdminPatchNotesNew',
      component: AdminPatchNotesNew
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    },
]

const router = createRouter({ history: createWebHistory(), routes })
export default router
