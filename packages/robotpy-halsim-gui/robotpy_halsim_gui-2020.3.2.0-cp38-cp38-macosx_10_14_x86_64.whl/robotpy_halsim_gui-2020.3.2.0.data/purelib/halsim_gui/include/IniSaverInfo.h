/*----------------------------------------------------------------------------*/
/* Copyright (c) 2020 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

#pragma once

#include <imgui.h>
#include <wpi/StringRef.h>

namespace halsimgui {

class NameInfo {
 public:
  NameInfo() { m_name[0] = '\0'; }

  bool HasName() const { return m_name[0] != '\0'; }
  const char* GetName() const { return m_name; }
  void GetName(char* buf, size_t size, const char* defaultName, int index);
  void GetName(char* buf, size_t size, const char* defaultName, int index,
               int index2);
  bool ReadIni(wpi::StringRef name, wpi::StringRef value);
  void WriteIni(ImGuiTextBuffer* out);
  void PushEditNameId(int index);
  void PopupEditName(int index);

 private:
  char m_name[64];
};

class OpenInfo {
 public:
  OpenInfo() = default;
  explicit OpenInfo(bool open) : m_open(open) {}

  bool IsOpen() const { return m_open; }
  void SetOpen(bool open) { m_open = open; }
  bool ReadIni(wpi::StringRef name, wpi::StringRef value);
  void WriteIni(ImGuiTextBuffer* out);

 private:
  bool m_open = false;
};

}  // namespace halsimgui
