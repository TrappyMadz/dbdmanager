export const patchNoteTypes = ['Bug Fix', 'Feature', 'Other'] as const

export type PatchNoteType = (typeof patchNoteTypes)[number]

export interface PatchNoteBase {
  version: string
  title: string
  content: string
  category: PatchNoteType
}

export type PatchNoteCreate = PatchNoteBase

export interface PatchNoteRead extends PatchNoteBase {
  id: string
  published_at: string
}

export type PatchNoteUpdate = Partial<PatchNoteBase>