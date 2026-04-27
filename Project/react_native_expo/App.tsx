import "./global.css";

import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import { SafeAreaView, ScrollView } from "react-native";

import { AuthShellLayout } from "./src/components/AuthShellLayout";
import { DashboardScreen } from "./src/screens/DashboardScreen";
import { LoginScreen } from "./src/screens/LoginScreen";
import { SignupScreen } from "./src/screens/SignupScreen";
import { initialAuthInput, type AuthInput, type Screen } from "./src/types/auth";

export default function App() {
  const [screen, setScreen] = useState<Screen>("login");
  const [input, setInput] = useState<AuthInput>(initialAuthInput);
  const [currentUser, setCurrentUser] = useState("Demo User");

  const submitLogin = () => {
    if (input.email.trim()) {
      setCurrentUser(input.email.split("@")[0] || "User");
    }
    setScreen("dashboard");
  };

  const submitSignup = () => {
    if (input.name.trim()) {
      setCurrentUser(input.name.trim());
    }
    setScreen("dashboard");
  };

  const signOut = () => {
    setInput(initialAuthInput);
    setScreen("login");
  };

  const handleUpdateInput = (key: keyof AuthInput, value: string) => {
    setInput((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-100">
      <StatusBar style="dark" />
      <ScrollView
        contentContainerClassName="min-h-full items-center justify-center p-4 md:p-10"
        keyboardShouldPersistTaps="handled"
      >
        <AuthShellLayout screen={screen}>
          {screen === "login" && (
            <LoginScreen
              input={input}
              onUpdateInput={handleUpdateInput}
              onLogin={submitLogin}
              onGoToSignup={() => setScreen("signup")}
            />
          )}

          {screen === "signup" && (
            <SignupScreen
              input={input}
              onUpdateInput={handleUpdateInput}
              onSignup={submitSignup}
              onGoToLogin={() => setScreen("login")}
            />
          )}

          {screen === "dashboard" && (
            <DashboardScreen userName={currentUser} onSignOut={signOut} />
          )}
        </AuthShellLayout>
      </ScrollView>
    </SafeAreaView>
  );
}
