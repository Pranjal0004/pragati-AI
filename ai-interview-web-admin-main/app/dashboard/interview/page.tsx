'use client';

import { useState, useEffect, useRef } from 'react';
import { Form, Input, Select, Button, Card, message } from 'antd';

export default function InterviewPage() {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const [form] = Form.useForm();
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [latestQuestion, setLatestQuestion] = useState('');
  const [lastReceived, setLastReceived] = useState('');
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [interviewTimer, setInterviewTimer] = useState(0);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [estimatedTime, setEstimatedTime] = useState(60);
  const [hint, setHint] = useState<string | null>(null);
  const [awaitingHintAck, setAwaitingHintAck] = useState(false);
  const [timeoutTriggered, setTimeoutTriggered] = useState(false);

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const interviewTimerRef = useRef<NodeJS.Timeout | null>(null);
  const timeoutTriggerRef = useRef(false);
  const lastTimerQuestionRef = useRef<string | null>(null);

  const startTimer = (seconds: number, questionId: string) => {
    // Prevent resetting the timer for the same question
    if (lastTimerQuestionRef.current === questionId) return;
  
    // Clear previous timer
    if (timerRef.current) clearInterval(timerRef.current);
  
    // Update refs and states
    lastTimerQuestionRef.current = questionId;
    timeoutTriggerRef.current = false;
    setTimeoutTriggered(false);
    setTimeLeft(seconds);
  
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev && prev <= 1) {
          clearInterval(timerRef.current!);
          triggerTimeout(); // guarded
          return 0;
        }
        return prev! - 1;
      });
    }, 1000);
  };  

  const stopInterviewTimer = () => {
    if (interviewTimerRef.current) {
      clearInterval(interviewTimerRef.current);
      interviewTimerRef.current = null;
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    lastTimerQuestionRef.current = null;
  };  

  const handleNewPayload = (payload: any, feedbackMsg?: string) => {
    const { question, acknowledgement, questionNumber, isComplete, estimatedTime: newTime, action, hint: hintText } = payload;
  
    if (action === "await_hint_acknowledgement" && hintText) {
      setHint(hintText);
      setAwaitingHintAck(true);
      return; 
    }
  
    if (question && question !== lastReceived) {
      const aiMessage = `AI: ${acknowledgement} Q${questionNumber}: ${question}`;
      setMessages(prev => [...prev, aiMessage]);
      setLatestQuestion(question);
      setEstimatedTime(newTime || 60);
      setLastReceived(question);
      setTimeoutTriggered(false);
      startTimer(newTime || 60, `${question}-${questionNumber}`);
    }    
  
    if (isComplete) {
      setInterviewComplete(true);
      stopInterviewTimer();
      if (feedbackMsg) setFeedback(feedbackMsg);
    }
  };  

  const triggerTimeout = async () => {
    console.log(("Inside trigger timeout"));
    
    if (timeoutTriggerRef.current) return; // prevent multiple calls
    timeoutTriggerRef.current = true; // mark as triggered
    setTimeoutTriggered(true); // UI-related state
    
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/handle-timeout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId }),
      });
      console.log('⏳ Timeout triggered');
      const data = await res.json();
      const payload = data?.new_state?.questionPayload;
  
      if (payload) {
        handleNewPayload(payload, data.feedback);
      } else {
        setMessages(prev => [...prev, '✅ Interview complete.']);
        setInterviewComplete(true);
        stopInterviewTimer();
        if (data.feedback) setFeedback(data.feedback);
      }
    } catch (err) {
      console.error('Failed to handle timeout:', err);
    }
  };
  

  const startInterview = async (values: any) => {
    setLoading(true);
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role: values.role,
          level: values.level,
          durationMinutes: values.duration,
        }),
      });

      const data = await res.json();
      setSessionId(data.sessionId);
      setMessages(data.messages || []);
      setInterviewTimer(0);

      if (interviewTimerRef.current) clearInterval(interviewTimerRef.current);
      interviewTimerRef.current = setInterval(() => {
        setInterviewTimer(prev => prev + 1);
      }, 1000);

      const initialPayload = data?.questionPayload;
      if (initialPayload) {
        handleNewPayload(initialPayload);
      }
    } catch (err) {
      message.error('Failed to start interview');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sendAnswer = async () => {
    if (!answer) return;
    setLoading(true);
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, answer }),
      });

      const data = await res.json();
      setMessages(prev => [...prev, `You: ${answer}`]);
      setAnswer('');

      const payload = data?.new_state?.questionPayload;
      if (payload) {
        handleNewPayload(payload, data.feedback);
      } else {
        setMessages(prev => [...prev, '✅ Interview complete.']);
        setInterviewComplete(true);
        stopInterviewTimer();
        if (data.feedback) setFeedback(data.feedback);
      }
    } catch (err) {
      message.error('Error submitting answer');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const acknowledgeHint = async () => {
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/acknowledge-hint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId }),
      });
  
      const data = await res.json();
      const payload = data?.new_state?.questionPayload;
  
      if (payload) {
        handleNewPayload(payload, data.feedback);
      }
  
      setAwaitingHintAck(false);
      setHint(null);
    } catch (err) {
      console.error('Failed to acknowledge hint:', err);
      message.error('Could not acknowledge hint.');
    }
  };  

  useEffect(() => {
    if (!sessionId || interviewComplete) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch('/api/receive-question');
        const data = await res.json();

        if (data?.isComplete) {
          setMessages(prev => [...prev, `AI: ${data.acknowledgement}`]);
          setInterviewComplete(true);
          setLatestQuestion('');
          setLastReceived('');
          setTimeLeft(null);
          stopInterviewTimer();
          if (data.feedback) setFeedback(data.feedback);
        } else if (data?.question && data.question !== lastReceived) {
          const payload = {
            question: data.question,
            acknowledgement: data.acknowledgement,
            questionNumber: data.questionNumber,
            estimatedTime: data.estimatedTime,
            isComplete: false,
          };
          handleNewPayload(payload, data.feedback);
        }
      } catch (err) {
        console.error('Polling failed', err);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [sessionId, lastReceived, interviewComplete]);



  return (
    <Card
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Start AI Interview</span>
          {sessionId && (
            <span style={{ fontSize: '0.9rem', color: '#555' }}>
              🕒 {Math.floor(interviewTimer / 60)}m {interviewTimer % 60}s
            </span>
          )}
        </div>
      }
      loading={loading}
    >
      {!sessionId ? (
        <Form form={form} layout="vertical" onFinish={startInterview}>
          <Form.Item name="role" label="Role" rules={[{ required: true }]}>
            <Input placeholder="e.g., Data Analyst" />
          </Form.Item>
          <Form.Item name="level" label="Level" rules={[{ required: true }]}>
            <Select placeholder="Select level">
              <Select.Option value="Entry">Entry</Select.Option>
              <Select.Option value="Mid">Mid</Select.Option>
              <Select.Option value="Senior">Senior</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="duration" label="Duration (in minutes)" rules={[{ required: true }]}>
            <Input type="number" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Start Interview
            </Button>
          </Form.Item>
        </Form>
      ) : (
        <>
          <div
            style={{
              border: '1px solid #ccc',
              padding: '1rem',
              marginBottom: '1rem',
              minHeight: 200,
              background: '#f7f7f7',
            }}
          >
            {messages.map((msg, index) => (
              <div key={index} style={{ marginBottom: 8 }}>{msg}</div>
            ))}
            {awaitingHintAck && hint && (
              <div style={{
                backgroundColor: '#fffbe6',
                border: '1px solid #ffe58f',
                borderRadius: 4,
                padding: '1rem',
                marginBottom: '1rem'
              }}>
                <strong>💡 Hint:</strong> {hint}
                <br />
                <Button type="dashed" onClick={acknowledgeHint} style={{ marginTop: '0.5rem' }}>
                  Got it
                </Button>
              </div>
            )}
            {interviewComplete && feedback && (
              <div style={{ marginTop: 20, padding: 10, background: '#e6f7ff', border: '1px solid #91d5ff', borderRadius: 4 }}>
                <strong>📝 Feedback:</strong>
                <div>{feedback}</div>
              </div>
            )}
          </div>

          {latestQuestion && timeLeft !== null && (
            <div style={{ marginBottom: 10, fontWeight: 'bold' }}>
              ⏳ Time remaining: {Math.floor(timeLeft / 60)}m {timeLeft % 60}s
            </div>
          )}

          <Input.TextArea
            value={answer}
            rows={2}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer..."
          />
          <Button
            type="primary"
            onClick={sendAnswer}
            disabled={!answer}
            style={{ marginTop: 10 }}
            loading={loading}
          >
            Send Answer
          </Button>
        </>
      )}
    </Card>
  );
}
