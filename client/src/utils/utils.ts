import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * tailwind-merge と clsx を組み合わせた関数
 * これを使用することで、tailwindcss のクラス名と他のクラス名を組み合わせることができる
 * 例: <div className={cn('text-red-500', 'bg-blue-500', 'text-lg', 'font-bold')}>Hello</div>
 * 条件によってクラス名を追加したり削除したりする場合は、clsx を使用し、
 * Tailwindのクラスがバッティングしないようにするために、twMerge を使用する
 * @param inputs 
 * @returns 
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
