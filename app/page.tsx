'use client';
import { AppShell,Splitter, rem, Group, Text, Container } from '@mantine/core';
import { useDisclosure, useHeadroom } from '@mantine/hooks';
import { mantineTheme } from './theme'
import { HeaderSimple } from '../components/layout/header'
import { TableauEditor } from '@/components/table_editor/tableEditor';
import Image from 'next/image'
import logo from './icon1.png'



export default function Home() {
  const [opened, { toggle }] = useDisclosure();
  const { pinned } = useHeadroom({ fixedAt: 120 });

  return (
  <AppShell 
    padding="sm"
    header={{height: 60 }}
    pt="sm"
    >
    <AppShell.Header  bg="yellow" className='flex items-center' >
      <Container h='100%' fluid className="flex items-center gap-4" >
       <Image src={logo} alt="Site Logo" width={45} style={{borderRadius:5}}/>
      <Text w="fit-content" h="fit-content" size='xl' bg="cyan"> Tableau Lab</Text>
      </Container>
    </AppShell.Header>

    <AppShell.Main bg="red" mt="x" pt="60">
      <div className="pt-60" style={{backgroundColor:"orange"}}>
    <Splitter bg="blue">
      <Splitter.Pane defaultSize={50} bg="blue">
        <TableauEditor/>
      </Splitter.Pane>
      <Splitter.Pane defaultSize={50} bg="teal">
        <TableauEditor/>
      </Splitter.Pane>
    </Splitter>
    </div>
    </AppShell.Main>
  </AppShell>
  
  );
}
