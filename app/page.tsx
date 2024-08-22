// app/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Zap, FileText, CheckCircle, Moon, Sun } from 'lucide-react'

export default function Home() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)

  useEffect(() => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setIsDarkMode(true)
    }
  }, [])

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
    }
  }, [isDarkMode])

  const handleHumanize = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/humanize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })
      const data = await response.json()
      setOutputText(data.paraphrased_text)
    } catch (error) {
      console.error('Error:', error)
      setOutputText('An error occurred while processing your text.')
    } finally {
      setIsLoading(false)
    }
  }

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
  }

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-gray-900' : 'bg-white'}`}>
      <div className="max-w-5xl mx-auto p-6">
        <div className="flex justify-end mb-4">
          <Button
            onClick={toggleDarkMode}
            variant="outline"
            size="icon"
            className={`rounded-full ${isDarkMode ? 'bg-gray-800 text-purple-400' : 'bg-white text-gray-800'}`}
          >
            {isDarkMode ? <Sun className="h-[1.2rem] w-[1.2rem]" /> : <Moon className="h-[1.2rem] w-[1.2rem]" />}
          </Button>
        </div>
        <div className="text-center mb-12">
          <h1 className={`text-5xl font-extrabold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
            AI Text <span className={isDarkMode ? 'text-purple-500' : 'text-orange-500'}>Humanizer</span>
          </h1>
          <p className={`text-xl max-w-2xl mx-auto ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Transform robotic AI content into natural, human-like text in seconds!
          </p>
        </div>

        <Card className={`mb-8 border-2 shadow-lg relative overflow-hidden ${isDarkMode ? 'bg-gray-800 border-purple-500' : 'bg-white border-orange-500'}`}>
          <div className={`absolute top-0 right-0 w-40 h-40 rounded-full transform translate-x-20 -translate-y-20 ${isDarkMode ? 'bg-purple-500' : 'bg-orange-500'}`}></div>
          <CardHeader className="relative z-10">
            <CardTitle className={`text-3xl font-bold flex items-center gap-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
              <Sparkles className={`w-8 h-8 ${isDarkMode ? 'text-purple-500' : 'text-orange-500'}`} />
              Start Humanizing
            </CardTitle>
            <CardDescription className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
              Paste your AI-generated content and watch the magic happen!
            </CardDescription>
          </CardHeader>
          <CardContent className="grid md:grid-cols-2 gap-6">
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>AI-Generated Text</label>
              <Textarea 
                placeholder="Enter your AI-generated text here..." 
                className={`min-h-[200px] ${isDarkMode ? 'bg-gray-700 text-white border-gray-600 focus:border-purple-500 focus:ring-purple-500' : 'bg-white text-gray-900 border-orange-200 focus:border-orange-500 focus:ring-orange-500'}`}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Humanized Text</label>
              <Textarea 
                placeholder="Humanized text will appear here..." 
                className={`min-h-[200px] ${isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-orange-50 text-gray-900 border-orange-200'}`}
                value={outputText}
                readOnly
              />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-center mb-12">
          <Button 
            size="lg" 
            onClick={handleHumanize} 
            className={`px-8 text-white font-bold py-3 rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg ${
              isDarkMode 
                ? 'bg-purple-500 hover:bg-purple-600' 
                : 'bg-orange-500 hover:bg-orange-600'
            } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Humanizing...' : 'Humanize Now'}
            <Zap className="ml-2 h-5 w-5" />
          </Button>
        </div>

        <div className="grid md:grid-cols-3 gap-6 text-center">
          {[
            { icon: FileText, title: "AI-Friendly", description: "Works with ChatGPT, Bard, Jasper, and more" },
            { icon: CheckCircle, title: "100% Original", description: "Achieve complete originality in your content" },
            { icon: Zap, title: "Lightning Fast", description: "Transform your text in mere seconds" }
          ].map((feature, index) => (
            <Card key={index} className={`border-t-4 shadow-md hover:shadow-lg transition-shadow ${
              isDarkMode 
                ? 'bg-gray-800 border-t-purple-500' 
                : 'bg-white border-t-orange-500'
            }`}>
              <CardContent className="pt-6">
                <feature.icon className={`w-12 h-12 mx-auto mb-4 ${isDarkMode ? 'text-purple-500' : 'text-orange-500'}`} />
                <h3 className={`text-lg font-semibold mb-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>{feature.title}</h3>
                <p className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}