import { Pressable, Text, View } from "react-native";

import type { AuthInput } from "../types/auth";
import { FormField } from "./FormField";

type AuthFormCardProps = {
  title: string;
  subtitle: string;
  showName: boolean;
  input: AuthInput;
  onUpdateInput: (key: keyof AuthInput, value: string) => void;
  primaryCta: string;
  secondaryCta: string;
  onPrimaryPress: () => void;
  onSecondaryPress: () => void;
};

export function AuthFormCard({
  title,
  subtitle,
  showName,
  input,
  onUpdateInput,
  primaryCta,
  secondaryCta,
  onPrimaryPress,
  onSecondaryPress,
}: AuthFormCardProps) {
  return (
    <View>
      <Text className="text-3xl font-bold text-slate-900">{title}</Text>
      <Text className="mt-2 text-slate-500">{subtitle}</Text>

      <View className="mt-6 gap-4">
        {showName && (
          <FormField
            label="Full name"
            value={input.name}
            onChangeText={(value) => onUpdateInput("name", value)}
            placeholder="Jane Doe"
          />
        )}

        <FormField
          label="Email"
          value={input.email}
          onChangeText={(value) => onUpdateInput("email", value)}
          placeholder="you@example.com"
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <FormField
          label="Password"
          value={input.password}
          onChangeText={(value) => onUpdateInput("password", value)}
          placeholder="••••••••"
          secureTextEntry
        />

        <Pressable
          className="mt-2 items-center rounded-xl bg-indigo-600 px-4 py-3 active:bg-indigo-700"
          onPress={onPrimaryPress}
        >
          <Text className="text-base font-semibold text-white">{primaryCta}</Text>
        </Pressable>

        <Pressable
          className="items-center rounded-xl border border-slate-300 px-4 py-3 active:bg-slate-100"
          onPress={onSecondaryPress}
        >
          <Text className="text-base font-medium text-slate-700">
            {secondaryCta}
          </Text>
        </Pressable>
      </View>
    </View>
  );
}
