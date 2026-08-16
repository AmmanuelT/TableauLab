import Image from 'next/image'
import { Group, AppShell, Text,Flex } from '@mantine/core'
import logo from '../../public/web-app-manifest-192x192.png'

export const SiteLogo = ({...props}) => {
  return (
    <Group {...props }gap="sm" className='ps-10' bg="grey">
      <Image src={logo} alt="Site Logo" width={28} style={{borderRadius:5}}/>
      <Text size='28'> Tableau Lab</Text>
    </Group>
  )
}



export const HeaderSimple = ({...props}) =>{
  return (
   


<></>


  )
}