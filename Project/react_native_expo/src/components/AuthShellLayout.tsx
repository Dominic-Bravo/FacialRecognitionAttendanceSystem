import type { ReactNode } from "react";
import { Text, View } from "react-native";

import type { Screen } from "../types/auth";

type AuthShellLayoutProps = {
  screen: Screen;
  children: ReactNode;
};

export function AuthShellLayout({ screen, children }: AuthShellLayoutProps) {
  return (
    <View className="w-full max-w-5xl flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm md:flex-row">
      <View className="w-full bg-indigo-700 px-6 py-10 md:w-2/5 md:px-8">
        <Text className="text-sm font-semibold uppercase tracking-wider text-indigo-200">
          Expo + NativeWind
        </Text>
        <Text className="mt-2 text-3xl font-bold leading-tight text-white">
          Responsive Auth Demo
        </Text>
        <Text className="mt-4 text-base text-indigo-100">
          Works on mobile and web with shared components and Tailwind classes.
        </Text>
        <View className="mt-6 rounded-xl bg-indigo-600/60 p-4">
          <Text className="text-indigo-100">
            Current screen:{" "}
            <Text className="font-semibold text-white">{screen}</Text>
          </Text>
        </View>
      </View>

      <View className="w-full p-6 md:w-3/5 md:p-8">{children}</View>
    </View>
  );
}
