import { Table } from "@mantine/core"


export const TableauEditor = () => {
    return (
        <>
            <Table withTableBorder>
                <Table.Tbody>
                    <Table.Tr>
                        <Table.Td>1</Table.Td>
                        <Table.Td>2</Table.Td>
                        <Table.Td>3</Table.Td>
                    </Table.Tr>
                    <Table.Tr>
                        <Table.Td>1</Table.Td>
                        <Table.Td>2</Table.Td>
                    </Table.Tr>
                    <Table.Tr>
                        <Table.Td>1</Table.Td>
                    </Table.Tr>
                </Table.Tbody>
            </Table>
        </>
    )
}