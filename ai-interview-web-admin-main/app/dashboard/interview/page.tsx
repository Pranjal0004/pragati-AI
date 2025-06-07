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
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const [interviewTimer, setInterviewTimer] = useState<number>(0);
  const interviewTimerRef = useRef<NodeJS.Timeout | null>(null);
  const [estimatedTime, setEstimatedTime] = useState(60);

  const triggerTimeout = async () => {
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/handle-timeout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId }),
      });
  
      const data = await res.json();
      console.log('⏱️ Timeout handled:', data);
  
      const newState = data?.new_state;
      const payload = newState?.questionPayload;
  
      if (payload) {
        const { question, acknowledgement, questionNumber, isComplete } = payload;
  
        // Only handle new question
        if (question !== lastReceived) {
          const tempMessage = `AI: ${acknowledgement} Q${questionNumber}: ${question}`;
          setMessages((prev) => [...prev, tempMessage]);
          setLatestQuestion(question);
          setEstimatedTime(payload.estimatedTime || 60);
          setLastReceived(question);
          startTimerForNewQuestion(payload.estimatedTime || 60);
        }
  
        if (isComplete) {
          setInterviewComplete(true);
          if (interviewTimerRef.current) {
            clearInterval(interviewTimerRef.current);
            interviewTimerRef.current = null;
          }
        }
      } else {
        setMessages((prev) => [...prev, '✅ Interview complete.']);
        setInterviewComplete(true);
        if (interviewTimerRef.current) {
          clearInterval(interviewTimerRef.current);
          interviewTimerRef.current = null;
        }
      }
    } catch (error) {
      console.error('Failed to handle timeout:', error);
    }
  };  

  const startTimerForNewQuestion = (seconds: number) => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  
    setTimeLeft(seconds); // this updates UI immediately
  
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev && prev <= 1) {
          clearInterval(timerRef.current!);
          timerRef.current = null;
          triggerTimeout();
          return 0;
        }
        return prev! - 1;
      });
    }, 1000);
  };  

  useEffect(() => {
    if (!lastReceived || interviewComplete) return;
    startTimerForNewQuestion(estimatedTime);
  }, [lastReceived]);  

  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0 || interviewComplete) return;
    if (timerRef.current) clearInterval(timerRef.current);
  
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev && prev <= 1) {
          clearInterval(timerRef.current!);
          timerRef.current = null;
          if (!interviewComplete) {
            triggerTimeout();
          }
  
          if (interviewTimerRef.current) {
            clearInterval(interviewTimerRef.current);
            interviewTimerRef.current = null;
          }
  
          return 0;
        }
        return prev! - 1;
      });
    }, 1000);
  
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [timeLeft, interviewComplete]);  

  useEffect(() => {
    if (interviewComplete && interviewTimerRef.current) {
      clearInterval(interviewTimerRef.current);
      interviewTimerRef.current = null;
    }
  }, [interviewComplete]);  

  useEffect(() => {
    if (!sessionId || interviewComplete) return;
  
    const interval = setInterval(async () => {
      try {
        const res = await fetch('/api/receive-question');
        const data = await res.json();
        console.log("📥 Polled data:", data);
  
        if (data?.isComplete) {
          setMessages((prev) => [...prev, `AI: ${data.acknowledgement}`]);
          setLatestQuestion('');
          setLastReceived('');
          setInterviewComplete(true); 
          setTimeLeft(null);
          return;
        }
        if (data?.question && data.question !== lastReceived) {
          const newMessages = [
            `AI: ${data.acknowledgement} Q${data.questionNumber}: ${data.question}`
          ];
          setMessages((prev) => [...prev, ...newMessages]);
          setLatestQuestion(data.question);
          setEstimatedTime(data.estimatedTime || 60);
          setLastReceived(data.question);
          const estimated = data.estimatedTime || data?.questionPayload?.estimatedTime || 60;
          startTimerForNewQuestion(estimated);
        }        
      } catch (err) {
        console.error("Polling failed", err);
      }
    }, 3000);
  
    return () => clearInterval(interval);
  }, [sessionId, lastReceived, interviewComplete]);  

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
      console.log("🎯 Start Interview Response:", data);
  
      setSessionId(data.sessionId);
      setInterviewTimer(0);
      if (interviewTimerRef.current) clearInterval(interviewTimerRef.current);
      interviewTimerRef.current = setInterval(() => {
        setInterviewTimer((prev) => prev + 1);
      }, 1000);

      const initialMessage = data.messages?.[0] || '';
      const match = initialMessage.match(/Q\d+: (.*)/); 
      const questionOnly = match ? match[1] : '';
  
      setMessages(data.messages || []);
      setLatestQuestion(questionOnly);
      setEstimatedTime(data.estimatedTime || 60);
      setLastReceived(data.question);
      setTimeLeft(data?.questionPayload?.estimatedTime || 60);
    } catch (error) {
      message.error('Failed to start interview');
      console.error('Fetch failed:', error);
    } finally {
      setLoading(false);
    }
  };  

  const sendAnswer = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${backendUrl}/api/v1/interview-graph/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          answer,
        }),
      });
  
      const data = await res.json();
      setMessages((prev) => [...prev, `You: ${answer}`]);
  
      const newState = data?.new_state;
      const payload = newState?.questionPayload;
  
      if (payload) {
        const { question, acknowledgement, questionNumber, isComplete } = payload;
  
        // Only handle new question
        if (question !== lastReceived) {
          const tempMessage = `AI: ${acknowledgement} Q${questionNumber}: ${question}`;
          setMessages((prev) => [...prev, tempMessage]);
          setLatestQuestion(question);
          setEstimatedTime(payload.estimatedTime || 60);
          setLastReceived(question);
          startTimerForNewQuestion(payload.estimatedTime || 60);
        }
  
        if (isComplete) {
          setInterviewComplete(true);
          if (interviewTimerRef.current) {
            clearInterval(interviewTimerRef.current);
            interviewTimerRef.current = null;
          }
        }
      } else {
        setMessages((prev) => [...prev, '✅ Interview complete.']);
        setInterviewComplete(true);
        if (interviewTimerRef.current) {
          clearInterval(interviewTimerRef.current);
          interviewTimerRef.current = null;
        }
      }
  
      setAnswer('');
    } catch (err) {
      console.error('Failed to send answer', err);
      message.error('Error submitting answer');
    } finally {
      setLoading(false);
    }
  };  

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
          <Form.Item
            name="role"
            label="Role"
            rules={[{ required: true, message: 'Please select a role' }]}
          >
            <Input placeholder="e.g., Data Analyst" />
          </Form.Item>

          <Form.Item
            name="level"
            label="Level"
            rules={[{ required: true, message: 'Please select a level' }]}
          >
            <Select placeholder="Select level">
              <Select.Option value="Entry">Entry</Select.Option>
              <Select.Option value="Mid">Mid</Select.Option>
              <Select.Option value="Senior">Senior</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="duration"
            label="Duration (in minutes)"
            rules={[{ required: true, message: 'Please enter a duration' }]}
          >
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
              <div key={index} style={{ marginBottom: 8 }}>
                {msg}
              </div>
            ))}
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
