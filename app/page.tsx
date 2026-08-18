"use client";
import { useState, useEffect } from 'react'; 
import { AppShell,Splitter,Paper, Title, rem, Group, Text, Container, useMantineTheme, useMantineColorScheme, useComputedColorScheme, Tooltip, ActionIcon, Stack, } from '@mantine/core';
import { Split } from '@gfazioli/mantine-split-pane';
import '@gfazioli/mantine-split-pane/styles.css';
import '@gfazioli/mantine-split-pane/styles.layer.css';
import { useDisclosure, useHeadroom } from '@mantine/hooks';
import { mantineTheme } from './theme'
import { HeaderSimple } from '../components/layout/header'
import { TableauEditor } from '@/components/tableau_editor/tableauEditor';
import Image from 'next/image'
import logo from './icon1.png'
import {
  IconBrandGithub,
  IconBrightnessUp, IconHelpCircle, IconMoon,
  IconSettings
} from "@tabler/icons-react";
//import Editor from '@monaco-editor/react';

const links = [
  { link: '', label: 'Home' },
  { link: '', label: 'Tutorial' },
  { link: '', label: 'Editor' },
];
import dynamic from 'next/dynamic'

import { Editor } from "@dgmjs/core";
import { DGMEditor } from "@dgmjs/react";


export default function Home() {
  const [opened, { toggle }] = useDisclosure();
  const { pinned } = useHeadroom({ fixedAt: 120 });
  const theme = useMantineTheme();
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });
  const [nextJsColorScheme, setNextJsColorScheme] = useState("light")
  const [helpOpened, setHelpOpened] = useState(false);
  useEffect(() => {
    setNextJsColorScheme(computedColorScheme)
  }, [computedColorScheme]);
  const destColorMode = computedColorScheme === "light" ? "dark" : "light"
  const activeStyle = {
  color: theme.primaryColor
  } 
  const items = links.map((link) => {
  const style = activeStyle
    return (
      <a
        key={link.label}
        href={link.link}
        style = {style}
        target={undefined}
      >
        {link.label}
      </a>
    )
  })


const CanvasEditorWithoutSSR = dynamic(
  () => import("@/components/CanvasEditor"),
  {
    ssr: false,
    loading: () => <p>Loading Infinite Canvas...</p>, // Optional skeleton loader
  }
);
// Dynamically import your editor with SSR disable

  const handleMount = async (editor: Editor) => {
    editor.newDoc();
    editor.fitToScreen();
    window.addEventListener("resize", () => {
      editor.fit();
    });
  };

  return (
  
      <CanvasEditorWithoutSSR />
    
  // <AppShell 
  //   padding="sm"
  //   header={{height: 60 }}
  //   pt="sm"
  //   >
  //   <AppShell.Header className='flex items-center justify-around' >
  //     <Group h='100%' className="flex items-center gap-4" >
  //      <Image src={logo} alt="Site Logo" width={45} style={{borderRadius:5}}/>
  //     <Title w="fit-content" visibleFrom="sm" h="fit-content" size='xl' > Tableau Lab</Title>
  //     </Group>
  //     <Group>
  //         {items}
  //       </Group>
  //       <Group>
  //         <Tooltip label="Source Code">
  //           <ActionIcon component={"a"} target="_blank" href={""} size={"lg"} variant="default" aria-label="Source Code">
  //             <IconBrandGithub style={{ width: '70%', height: '70%' }} stroke={1.5} />
  //           </ActionIcon>
  //         </Tooltip>



  //         <Tooltip label="Help">
  //           <ActionIcon onClick={() => setHelpOpened(true)} size={"lg"} variant="default" aria-label="Help">
  //             <IconHelpCircle style={{ width: '70%', height: '70%' }} stroke={1.5} />
  //           </ActionIcon>
  //         </Tooltip>

  //         <Tooltip label={`Switch to ${destColorMode} mode`}>
  //           <ActionIcon size={"lg"} onClick={() => setColorScheme(destColorMode)} variant="default" aria-label="Toggle Color Mode">
  //             {
  //               nextJsColorScheme === "light"
  //                 ? <IconMoon style={{ width: '70%', height: '70%' }} stroke={1.5} />
  //                 : <IconBrightnessUp style={{ width: '70%', height: '70%' }} stroke={1.5} />
  //             }
  //           </ActionIcon>
  //         </Tooltip>
  //       </Group>
  //   </AppShell.Header>

  //   <AppShell.Main h="100%">
  //     <Stack h="100%">
  //   <Split autoResizers w="100%" h="100%">
  //     <Split.Pane w="100%" h="80vh">
  //       <Paper  withBorder w="100%" h="90vh">
  //           <Editor theme={destColorMode=== "light" ? "vs-dark": "light" } defaultLanguage="latex" defaultValue="// some comment" />
  //         </Paper>
  //     </Split.Pane>
  //     <Split.Resizer h="70%"/>
  //     <Split.Pane w="100%" h="90%" >
  //       <Paper >
  //       <TableauEditor size={10} />
  //       </Paper>
  //     </Split.Pane>
  //   </Split>
  //   </Stack>
  //   </AppShell.Main>
  // </AppShell>
  
  );
}
