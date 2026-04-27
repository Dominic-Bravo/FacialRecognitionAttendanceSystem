import { Pressable, Text, View } from "react-native";

import { InfoTile } from "../components/InfoTile";

type DashboardScreenProps = {
  userName: string;
  onSignOut: () => void;
};

export function DashboardScreen({ userName, onSignOut }: DashboardScreenProps) {
  return (
    <View>
      <Text className="text-3xl font-bold text-slate-900">Dashboard</Text>
      <Text className="mt-2 text-slate-500">
        Hi {userName}, your cross-platform app is running.
      </Text>

      <View className="mt-6 flex-row flex-wrap gap-3">
        <InfoTile title="Devices" value="Web + Mobile" />
        <InfoTile title="Framework" value="Expo + RN" />
        <InfoTile title="Styling" value="NativeWind" />
      </View>

      <Pressable
        className="mt-8 items-center rounded-xl bg-slate-900 px-4 py-3 active:bg-slate-700"
        onPress={onSignOut}
      >
        <Text className="text-base font-semibold text-white">Sign Out</Text>
      </Pressable>
    </View>
  );
}
