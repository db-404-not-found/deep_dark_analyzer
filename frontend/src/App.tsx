import { useMemo, useState } from "react"
import styles from './app.module.scss'
import { useMutation, useQuery, useQueryClient } from 'react-query'
import {  toast } from 'react-toastify'
import { sendToAnalyze, fetchResult} from "./fetch"

type State = 'QUEUED' | 'STARTED' | 'RESPONSED' | ''
type Index = [number, number]
type Result = {
  indexes: Index[];
  estimation: string;
} | Record<string, never>

interface QueryData {
  id: string;
  status: State;
  result: Result;
}

const replaceText = (text: string, indices: Index[]) => {
  let res = text
  for (let [first, second] of indices.reverse()) {
    res = res.slice(0, first) +`<span class=\'${styles.highlight}\'>` + res.slice(first, second) + '</span>' + res.slice(second)
  }
  return {
    __html: res
  }
}

const refetchInterval = import.meta.env.VITE_REFETCH_INTERVAL_IN_SECONDS * 1000 || 5000

function App() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState<Result>({})

  const [currentState, setCurrentState] = useState<State>('')

  const [currentId, setCurrentId] = useState('')
  const client = useQueryClient()

  const {mutate: send, data: dataFromMutation} = useMutation({
    mutationFn: sendToAnalyze,
    onMutate() {
      setCurrentState('QUEUED')
    },
    onSuccess(data: QueryData) {
      client.invalidateQueries('text')
      setCurrentId(data.id)
      setCurrentState(data.status)

      if (data.status === 'RESPONSED') {
        setOutput(data.result)
      }
    },
    onError: () => {
      toast("Произошла ошибка", {
        type: 'error'
      })
    }
  })

  const replacer = useMemo(() => {
    if (output.indexes) {
      return replaceText(input, output.indexes)
    }
    return {
      __html: ""
    }
  }, [output])

  useQuery({
    enabled: !!dataFromMutation && currentState !== 'RESPONSED',
    queryFn: () => fetchResult(currentId),
    queryKey: ['text'],
    onSuccess(data: QueryData) {
      if (data.status === 'RESPONSED') {
        setOutput(data.result)
        setCurrentState(data.status)
      }
    },
    refetchInterval: refetchInterval
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
          <button 
            className={styles.button} 
            onClick={onClick} 
            disabled={currentState === 'STARTED' || currentState === 'QUEUED'} 
            type="button"
          >
            Анализ
          </button>
        </div>
        <div className={styles.wrapper}>
          <div className={styles.output}>
            {(currentState === 'STARTED' || currentState === 'QUEUED') && <span>Loading...</span>}
            {(currentState === 'RESPONSED') && <>
                <p dangerouslySetInnerHTML={replacer} className={styles.paragraph}>
                </p>   
            </>}
          </div>
          {(currentState === 'RESPONSED') && <div className={styles.press}>Оценка рейтинга пресс-релиза: {output.estimation}</div>}
        </div>
      </div>
    </main>
  )
}

export default App
