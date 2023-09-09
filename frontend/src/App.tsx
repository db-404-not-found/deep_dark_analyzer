import { useState } from "react"
import styles from './app.module.scss'
import { useMutation, useQuery, useQueryClient } from 'react-query'
import {  toast } from 'react-toastify'
import { sendToAnalyze, fetchResult} from "./fetch"

function App() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const client = useQueryClient()

  const {mutate: send, isLoading: isSending} = useMutation({
    mutationFn: sendToAnalyze,
    onSuccess() {
      client.invalidateQueries('text')
    },
    onError: () => {
      toast("Произошла ошибка", {
        type: 'error'
      })
    }
  })

  useQuery({
    queryFn: fetchResult,
    queryKey: ['text'],
    onSuccess(data) {
      setOutput(data)
    },
  })

  const onClick = () => {
    send(input)
  }

  return (
    <main>
      <header className={styles.header}>
        <h1 className={styles.headertext}>
          Text analyzer 1.0
        </h1>
      </header>
      <div className={styles.textareas}>
        <div className={styles.wrapper}>
          <textarea className={styles.input} value={input} onChange={e => setInput(e.target.value)} placeholder="Введите текст..."/>
          <button className={styles.button} onClick={onClick} disabled={isSending} type="button">
            Анализ
          </button>
        </div>
        <div className={styles.wrapper}>
          <textarea className={styles.output} value={output} readOnly placeholder="Здесь появится результат анализа"/>
        </div>
      </div>
    </main>
  )
}

export default App
